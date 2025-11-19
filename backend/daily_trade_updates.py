import os
from datetime import datetime, timedelta
import finnhub
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from server.models import Trade, Committee, CommitteeMembership
from get_stock_prices import save_current_prices
from get_trades import Scraper
from django.core.management.base import BaseCommand
import os
import time
from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# Initialize Alpaca client
alpaca_client = StockHistoricalDataClient(
    os.environ["ALPACA_API_KEY"], os.environ["ALPACA_API_SECRET"]
)


finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))


class Command(BaseCommand):
    help = "Runs daily trade updates, gets new trades and updates prices"

    def handle(self, *args, **options):
        print("Starting daily trade updates at ", datetime.now())
        try:
            s = Scraper()
            s.scrape()
            s.insert_trades()
            print("Trades successfully added")
        except Exception as e:
            print("Something failed: ", e)
        flag_trades()
        save_stock_prices()
        save_current_prices()


def get_next_day(date: datetime) -> datetime:
    return date + timedelta(days=1)


def get_stock_price(ticker: str, date: str) -> float:
    time.sleep(0.25)

    # Handle edge case adjustment
    if date == "2025-01-09":
        date = "2025-01-10"

    date = datetime.strptime(date, "%Y-%m-%d")

    # Adjust if weekend → move to Monday
    if date.weekday() == 5:  # Saturday → Monday
        date += timedelta(days=2)
    elif date.weekday() == 6:  # Sunday → Monday
        date += timedelta(days=1)

    start = date
    end = get_next_day(date)

    # Request daily bars
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame(amount=1, unit=TimeFrame.Hour),
        start=start,
        end=end,
    )

    bars = alpaca_client.get_stock_bars(request_params)

    if bars:
        return bars.data[ticker][0].close
    else:
        print("No historical data found for ", ticker)
        return -1


def save_stock_prices():
    trades = Trade.objects.filter(price_at_trade__lte=0).exclude(stock_id="N/A")
    print(len(trades))
    for trade in trades:
        try:
            price = get_stock_price(trade.stock.ticker, str(trade.date))
            trade.price_at_trade = price
            trade.save()
        except Exception as e:
            print(
                f"Failed to get trade {trade.id} with ticker: {trade.stock.ticker} with error {str(e)}"
            )
    print("Updated price data")


def flag_trades():
    trades = Trade.objects.filter(checked=False)
    count = 0
    for trade in trades:
        trade_sector = trade.stock.sector
        member = trade.member
        membership = CommitteeMembership.objects.filter(member_id=member.bio_guide_id)
        for m in membership:
            if m.committee.sector == trade_sector:
                trade.flagged = True
        trade.checked = True
        trade.save()
        count += 1
    # Trade.objects.filter(price_per_share=-1).delete()
    print(f"Updated flag on {count} trades")


if __name__ == "__main__":
    # print("Starting daily trade updates at ", datetime.now())
    # try:
    #     s = Scraper()
    #     s.scrape()
    #     s.insert_trades()
    #     print("Trades successfully added")
    # except Exception as e:
    #     print("Something failed: ", e)
    # flag_trades()
    # save_stock_prices()
    save_current_prices()
