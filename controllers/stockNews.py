import dotenv
import os
import requests
from datetime import datetime, timedelta

dotenv.load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

session = requests.Session()
session.headers.update({"User-Agent": "Chrome/122.0.0.0"})


def fetch_news():
    """Fetch India-focused market news using NewsAPI with graceful fallback."""
    try:
        if NEWS_API_KEY:
            yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
            params = {
                "q": "(India OR Indian) AND (stock market OR NSE OR BSE OR Sensex OR Nifty)",
                "from": yesterday,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 10,
                "apiKey": NEWS_API_KEY,
            }
            response = session.get("https://newsapi.org/v2/everything", params=params, timeout=15)
            response.raise_for_status()
            payload = response.json()
            articles = payload.get("articles", [])
            news_stack = []
            for item in articles:
                title = item.get("title")
                url = item.get("url")
                if title and url:
                    news_stack.append([title, url])
            if news_stack:
                print("Data fetching done successfully!")
                return news_stack

        # Fallback: curated India finance links when key is missing/empty response
        return [
            ["NSE India - Market News", "https://www.nseindia.com/market-data/latest-news"],
            ["BSE India - Corporate Announcements", "https://www.bseindia.com/corporates/ann.html"],
            ["Moneycontrol - Markets", "https://www.moneycontrol.com/stocksmarketsindia/"],
            ["Economic Times - Markets", "https://economictimes.indiatimes.com/markets"],
            ["Mint - Markets", "https://www.livemint.com/market"],
        ]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return [
            ["NSE India - Market News", "https://www.nseindia.com/market-data/latest-news"],
            ["BSE India - Corporate Announcements", "https://www.bseindia.com/corporates/ann.html"],
        ]
