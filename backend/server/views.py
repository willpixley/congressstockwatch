from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

from server.models import Stock, Trade, CongressMember, Sector
from django.forms.models import model_to_dict
from utils.members import get_trade_for_member
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import pandas as pd
from server.models import Trade, Committee, CommitteeMembership
from get_stock_prices import save_current_prices
from get_trades import Scraper
from daily_trade_updates import flag_trades, save_stock_prices
from datetime import datetime, timedelta
import os
import alpaca_trade_api as tradeapi
import threading
import logging


alpaca = tradeapi.REST(
    os.environ.get("ALPACA_API_KEY"),
    os.environ.get("ALPACA_API_SECRET"),
    base_url=os.environ.get("ALPACA_API_ENDPOINT"),
)

logger = logging.getLogger(__name__)


def run_daily_updates(request):
    if request.method == "GET":

        def updates():
            try:
                print("Starting daily trade updates at ", datetime.now())
                try:
                    s = Scraper(pages=30)
                    s.scrape()
                    s.insert_trades()
                    print("Trades successfully added")
                except Exception as e:
                    print("Something failed: ", e)
                flag_trades()
                save_stock_prices()
                save_current_prices()
                print("Daily updates successful")

            except Exception as e:
                print("Error during daily updates: %s", str(e))

        try:
            threading.Thread(target=updates).start()
            return JsonResponse({"status": "started"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid method"}, status=405)


def test_db(request):
    pass


def get_ticker(request):
    if request.method == "GET":
        search_param = request.GET.get("search", "")  # Get query param

        results = Stock.objects.filter(name__icontains=search_param).values()
        return JsonResponse({"data": list(results)}, safe=False)


def get_trades(request):
    if request.method == "GET":
        search_param = request.GET.get("trade_id", "")  # Get query param
        if search_param:
            trade = Trade.objects.get(id=search_param)
            trade_dict = model_to_dict(trade)
            trade_dict["updated_at"] = trade.updated_at

            # Add related objects as dictionaries
            trade_dict["member"] = model_to_dict(
                trade.member
            )  # Assuming ForeignKey to Member model
            trade_dict["stock"] = model_to_dict(trade.stock)
            trade_dict["sector"] = model_to_dict(trade.stock.sector)
            return JsonResponse(trade_dict)
        else:
            results = (
                Trade.objects.select_related("member", "stock")
                .order_by("-date")[:50]
                .values(
                    "id",
                    "price_at_trade",
                    "current_price",
                    "date",
                    "type",
                    "flagged",
                    "member__first_name",
                    "member__last_name",
                    "member__bio_guide_id",
                    "member__party",
                    "stock__ticker",
                    "stock__name",
                    "amount",
                    "traded_by",
                )
            )

            return JsonResponse({"results": list(results)})


def get_flagged_trades(request):
    if request.method == "GET":
        results = (
            Trade.objects.filter(flagged=True)
            .select_related("member", "stock")
            .order_by("-date")
            .values(
                "id",
                "price_at_trade",
                "current_price",
                "date",
                "type",
                "flagged",
                "member__first_name",
                "member__last_name",
                "member__bio_guide_id",
                "member__party",
                "stock__ticker",
                "stock__name",
                "amount",
                "traded_by",
            )
        )

        return JsonResponse({"results": list(results)})


def get_member_trades(request):
    try:
        if request.method == "GET":

            id = request.GET.get("id")
            results, history = get_trade_for_member(id)
            return JsonResponse(
                {"trades": list(results), "history": history}, safe=False
            )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_members(request):
    try:
        if request.method == "GET":
            members = CongressMember.objects.all().values()
            data = []
            for member in members:
                _, history = get_trade_for_member(member["bio_guide_id"])
                history["member"] = member
                data.append(history)
            data = sorted(data, key=lambda x: x["weighted_return"], reverse=True)

            return JsonResponse({"members": list(data[:25])}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Returns volume bought, sold, most common stock bought, most common stock sold, most bought industry, mnost sold industry (all last month)
def get_market_trends(request):
    try:
        volume_bought = 0
        volume_sold = 0
        industry_bought_count = {}
        industry_sold_count = {}
        one_month_ago = timezone.now() - relativedelta(months=1)
        recent_trades = Trade.objects.filter(date__gte=one_month_ago)
        for trade in recent_trades:
            trade_sector = trade.stock.sector.sector_code
            if trade.type == "b":
                volume_bought += trade.amount
                if trade_sector not in industry_bought_count:
                    industry_bought_count[trade_sector] = 1
                else:
                    industry_bought_count[trade_sector] += 1
            if trade.type == "s":
                volume_sold += trade.amount
                if trade_sector not in industry_sold_count:
                    industry_sold_count[trade_sector] = 1
                else:
                    industry_sold_count[trade_sector] += 1
        max_sector_bought = max(industry_bought_count, key=industry_bought_count.get)
        max_sector_sold = max(industry_sold_count, key=industry_sold_count.get)
        max_sector_bought = model_to_dict(
            Sector.objects.get(sector_code=max_sector_bought)
        )
        max_sector_sold = model_to_dict(Sector.objects.get(sector_code=max_sector_sold))

        return JsonResponse(
            {
                "volume_bought": volume_bought,
                "volume_sold": volume_sold,
                "max_sector_bought": max_sector_bought,
                "max_sector_sold": max_sector_sold,
                "since": one_month_ago,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
