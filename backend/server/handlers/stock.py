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
import requests

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")  # or hardcode your key as a string
alpaca = tradeapi.REST(
    os.environ.get("ALPACA_API_KEY"),
    os.environ.get("ALPACA_API_SECRET"),
    base_url=os.environ.get("ALPACA_API_ENDPOINT"),
)


def get_stock_history(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=405)

    ticker = request.GET.get("ticker")
    if not ticker:
        return JsonResponse({"error": "Missing ticker"}, status=400)

    try:
        # Define ~6 months back
        end = datetime.today().date() - timedelta(days=2)
        start = end - timedelta(days=6 * 30)

        # Fetch daily bars
        bars = alpaca.get_bars(
            ticker,
            "1Day",
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
        ).df

        if not bars.empty:
            dates = bars.index.strftime("%Y-%m-%d").tolist()
            prices = bars["close"].tolist()
        else:
            dates, prices = [], []

        data = {
            "dates": dates,
            "prices": prices,
        }
        return JsonResponse({"data": data})

    except tradeapi.rest.APIError as e:
        # Handles restricted access errors for free tier
        return JsonResponse({"error": f"Alpaca API error: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_stock_news(req):
    try:
        """
        Fetch stock news from Finnhub for a given ticker (last 3 months)
        """
        if not FINNHUB_API_KEY:
            return JsonResponse(
                {"error": "Missing FINNHUB_API_KEY"},
                status=500,
            )
        ticker = req.GET.get("ticker")
        today = datetime.today()
        three_months_ago = today - timedelta(days=90)

        formatted_present = today.strftime("%Y-%m-%d")
        formatted_past = three_months_ago.strftime("%Y-%m-%d")

        params = {
            "token": FINNHUB_API_KEY,
            "symbol": ticker,
            "from": formatted_past,
            "to": formatted_present,
        }

        try:
            resp = requests.get("https://finnhub.io/api/v1/company-news", params=params)
            resp.raise_for_status()
            return JsonResponse(resp.json(), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)


def get_stock_profile(req):
    if not FINNHUB_API_KEY:
        return JsonResponse({"error": "Missing FINNHUB_API_KEY"}, status=500)
    ticker = req.GET.get("ticker")

    params = {
        "token": FINNHUB_API_KEY,
        "symbol": ticker,
    }

    try:
        resp = requests.get("https://finnhub.io/api/v1/stock/profile2", params=params)
        resp.raise_for_status()
        return JsonResponse(resp.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
