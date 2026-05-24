import yfinance as yf
import requests
import time
from typing import List

session = requests.Session()
session.headers.update({"User-Agent": "Chrome/122.0.0.0"})


def normalize_symbol(symbol: str) -> str:
    """Default plain symbols to NSE for India-first behavior."""
    s = (symbol or "").strip().upper()
    if not s:
        return s
    if "." in s:
        return s
    return f"{s}.NS"


def get_top_stock_info() -> List[dict]:
    # Indian large-cap and liquid names (NSE)
    tickers_list = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS",
        "INFY.NS", "SBIN.NS", "LT.NS", "ITC.NS", "HINDUNILVR.NS",
        "KOTAKBANK.NS", "AXISBANK.NS", "BAJFINANCE.NS", "ASIANPAINT.NS", "MARUTI.NS",
        "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "WIPRO.NS",
        "ADANIPORTS.NS", "POWERGRID.NS", "NTPC.NS", "ONGC.NS", "TATAMOTORS.NS",
        "M&M.NS", "TECHM.NS", "HCLTECH.NS", "INDUSINDBK.NS", "BAJAJFINSV.NS"
    ]
    stock_data = []
    try:
        data = yf.download(tickers_list, period="2d", interval="1d", group_by='ticker', auto_adjust=True)
        changes = []

        for ticker in tickers_list:
            try:
                close_prices = data[ticker]['Close']
                percent_change = ((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2]) * 100
                changes.append((ticker, round(percent_change, 2)))
            except Exception:
                continue

        # Sort by absolute percent change and pick top 5 movers
        top_5_tickers = [ticker for ticker, _ in sorted(changes, key=lambda x: abs(x[1]), reverse=True)[:5]]
        tickers = yf.Tickers(top_5_tickers)
        while top_5_tickers:
            try:
                stock = top_5_tickers.pop()
                info = tickers.tickers[stock].info
                stock_info = {
                    'symbol': stock,
                    'name': info.get('shortName', 'N/A'),
                    'currentPrice': info.get('currentPrice', 'N/A'),
                    'previousClose': info.get('previousClose', 'N/A'),
                    'sector': info.get('sector', 'N/A'),
                    'currency': info.get('currency', 'INR'),
                    'exchange': info.get('exchange', 'NSE')
                }
                stock_data.append(stock_info)
            except Exception as e:
                print(f"Could not fetch info for {stock}: {e}")

        print("Data fetching done successfully!")
        return stock_data

    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return []


def get_stock(symbol):
    try:
        normalized_symbol = normalize_symbol(symbol)
        stock = yf.Ticker(normalized_symbol)
        info = stock.info
        stock_info = {
            'symbol': normalized_symbol,
            'name': info.get('shortName', 'N/A'),
            'currentPrice': info.get('currentPrice', 'N/A'),
            'previousClose': info.get('previousClose', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'currency': info.get('currency', 'INR'),
            'exchange': info.get('exchange', 'NSE')
        }
        print("Data fetching done successfully!")
        return stock_info
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        time.sleep(5)
        return {
            'symbol': normalize_symbol(symbol),
            'name': 'N/A',
            'currentPrice': 'N/A',
            'previousClose': 'N/A',
            'sector': 'N/A',
            'currency': 'INR',
            'exchange': 'NSE'
        }
