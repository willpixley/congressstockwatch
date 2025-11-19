import requests
from bs4 import BeautifulSoup
import time
import datetime as dt


import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from server.models import Stock, CongressMember, Trade


months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def range_to_avg(value: str) -> int:
    ranges = {
        "< 1K": 500,  # Average of 0 and 1000
        "1K–15K": (1000 + 15000) // 2,
        "15K–50K": (15000 + 50000) // 2,
        "50K–100K": (50000 + 100000) // 2,
        "100K–250K": (100000 + 250000) // 2,
        "250K–500K": (250000 + 500000) // 2,
        "500K–1M": (500000 + 1000000) // 2,
        "1M–5M": (1000000 + 5000000) // 2,
        "5M–25M": (5000000 + 25000000) // 2,
        "25M–50M": (25000000 + 50000000) // 2,
    }

    return ranges.get(value, None)  # Return None if value not found


class Scraper:
    def __init__(self, pages=30) -> None:
        self.pages = pages
        self.url = "https://www.capitoltrades.com/trades?page={}"
        self.tradeList = []

    def scrape(self) -> None:
        for i in range(1, self.pages):
            url = self.url.format(i)
            page = Page(url)
            pageInfo = page.get_page_info()
            self.tradeList.extend(pageInfo)

    def insert_trades(self):
        Trade.objects.bulk_create(self.tradeList, ignore_conflicts=True)
        print(f"Added {len(self.tradeList)} trades")


class Page:
    def __init__(self, url) -> None:
        self.url = url

    def fetch_page(self):
        """Fetch the HTML content of the page."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails
        return response.text

    def get_page_info(self) -> list:
        trade_list = []
        html_content = self.fetch_page()
        soup = BeautifulSoup(html_content, "html.parser")

        trades = soup.select("table tbody tr")  # Select all trade rows

        for trade in trades:

            try:
                trade_data = self._extract_trade_data(trade)
                if trade_data and trade_data.stock.ticker != "N/A":
                    trade_list.append(trade_data)
            except Exception as e:
                print("Failed to get a trade", str(e))

        return trade_list

    def _extract_trade_data(self, trade):
        """Extract specific trade details from a row."""
        name_element = trade.select_one("td:nth-of-type(1) h2 a")
        ticker_element = trade.select_one(".issuer-ticker")
        type_element = trade.select_one("[class*=tx-type--]")
        date_element = trade.select_one("td:nth-of-type(4) div div")
        size_element = trade.select_one(".q-field.trade-size")
        owner_element = trade.select_one(".owner-with-icon")
        link_element = trade.select_one("td:nth-of-type(10) button a")

        if not name_element or not link_element:
            return None

        link = link_element["href"]
        trade_id = link.split("/")[-1]
        bio_guide_id = name_element["href"].split("/")[-1]
        full_name = name_element.text.strip().split()
        first_name = full_name[0]
        last_name = full_name[-1]

        date_text = date_element.text.replace("\n", " ").split()
        trade_date = dt.datetime(
            year=int(date_text[1][-4:]),
            month=months[date_text[1][:3]],
            day=int(date_text[0]),
        )

        ticker = ticker_element.text.split(":")[0] if ticker_element else "N/A"
        trade_type = type_element.text[0] if type_element else "?"
        trade_size = range_to_avg(size_element.text.strip()) if size_element else None
        owner = owner_element.text if owner_element else "Unknown"

        try:
            member = CongressMember.objects.get(bio_guide_id=bio_guide_id)
        except:
            print(f"Failed to get member id: {bio_guide_id} ")
            raise Exception
        try:
            stock = Stock.objects.get(ticker=ticker)
        except Exception as e:
            print(
                f"Failed to get a stock ticker while scraping. Ticker: {ticker} with error {str(e)}"
            )
            raise Exception

        return Trade(
            id=trade_id,
            type=trade_type,
            stock=stock,
            member=member,
            traded_by=owner,
            date=trade_date,
            amount=trade_size,
        )


if __name__ == "__main__":
    try:
        s = Scraper()
        s.scrape()
        s.insert_trades()
        print("Trades successfully added")
    except Exception as e:
        print("Something failed: ", e)
