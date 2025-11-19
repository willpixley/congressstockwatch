import os
import django
import finnhub
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from server.models import Trade, Committee, CommitteeMembership

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

import pandas as pd
from io import StringIO
from django.db import transaction


import requests


def fetch_bulk_prices_via_nasdaq_api():
    """
    Fetches bulk stock price data from Nasdaq API.
    Returns a dict {ticker: price}.
    """
    url = (
        "https://api.nasdaq.com/api/screener/stocks" "?tableonly=true" "&download=true"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    j = resp.json()

    # The JSON structure has headers + rows
    rows = j["data"]["rows"]

    price_map = {}
    for row in rows:
        try:
            ticker = str(row["symbol"]).upper()
            # Adjust the key names if they differ
            price_str = row["lastsale"]  # or maybe row["LastSale"]
            # Clean the price (remove $, commas)
            price = float(price_str.replace("$", "").replace(",", ""))
            price_map[ticker] = price
        except Exception:
            continue

    return price_map


def save_current_prices():
    # 1. Download bulk prices
    price_map = fetch_bulk_prices_via_nasdaq_api()
    print("Got price map")

    # 2. Filter trades needing update
    trades = Trade.objects.filter(price_at_trade__gt=0)
    updated = []
    missing = set()

    for i, trade in enumerate(trades):
        if i % 100 == 0:
            print(f"Processed {i} trades")
        ticker = trade.stock.ticker.upper()
        if ticker in price_map:
            trade.current_price = price_map[ticker]
            updated.append(trade)
        else:
            missing.add(ticker)

    # 3. Bulk update
    if updated:
        Trade.objects.bulk_update(updated, ["current_price"])

    # Logging
    print("Updated", len(updated), "trades.")
    if missing:
        print("Missing tickers:", missing)
    print("Done.")


# def get_current_price(ticker: str) -> float:
#     # Handle special case mapping

#     quote = finnhub_client.quote(ticker)
#     print(f"Current price of {ticker} is {quote["c"]}")
#     # 'c' = current price
#     return quote["c"]


# def save_current_prices():
#     checked = {}
#     trades = Trade.objects.filter(price_at_trade__gt=0)
#     print(trades)
#     for trade in trades:
#         time.sleep(1)
#         if trade.stock.ticker not in checked:
#             try:
#                 current = get_current_price(trade.stock.ticker)
#                 trade.current_price = current
#                 checked[trade.stock.ticker] = current
#                 trade.save()

#             except Exception as e:
#                 print("ticker failed", trade.stock.ticker, "with", str(e))
#         else:
#             trade.current_price = checked[trade.stock.ticker]
#             trade.save()
#     print("Done")


if __name__ == "__main__":
    save_current_prices()
