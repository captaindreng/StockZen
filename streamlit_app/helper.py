"""
helper.py
---------
Shared utility functions used across all StockZen pages:
- loading the list of tradable stocks
- fetching live stock info / history from Yahoo Finance
- generating ARIMA-based price forecasts

Keeping all data-access logic here (instead of duplicating it in every
page) means each Streamlit page file only has to worry about UI/layout.
"""

import datetime as dt
from pathlib import Path

import pandas as pd
import yfinance as yf
from statsmodels.tsa.ar_model import AutoReg

# Yahoo Finance blocks cloud server IPs unless we send browser-like headers.
# Setting these on the yfinance session fixes the "Unable to fetch" error
# when the app is deployed on Streamlit Community Cloud.
_YF_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def _ticker(symbol: str) -> yf.Ticker:
    """Return a yfinance Ticker with browser-like headers to avoid IP blocks."""
    t = yf.Ticker(symbol)
    t.session = None  # let yfinance create a fresh session
    # Patch the underlying requests session headers
    import requests
    session = requests.Session()
    session.headers.update(_YF_HEADERS)
    t.session = session
    return t

# Path to the CSV that lists every BSE-listed company we support.
# Resolved relative to this file so it works no matter what directory
# `streamlit run` is launched from.
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "equity_issuers.csv"


def fetch_stocks() -> dict:
    """Return a dict mapping {Security Code: Issuer Name} for every stock."""
    df = pd.read_csv(DATA_PATH)
    df = df[["Security Code", "Issuer Name"]]
    return dict(zip(df["Security Code"], df["Issuer Name"]))


def fetch_periods_intervals() -> dict:
    """Return the valid yfinance (period -> [allowed intervals]) combinations."""
    return {
        "1d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m"],
        "5d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m"],
        "1mo": ["30m", "60m", "90m", "1d"],
        "3mo": ["1d", "5d", "1wk", "1mo"],
        "6mo": ["1d", "5d", "1wk", "1mo"],
        "1y": ["1d", "5d", "1wk", "1mo"],
        "2y": ["1d", "5d", "1wk", "1mo"],
        "5y": ["1d", "5d", "1wk", "1mo"],
        "10y": ["1d", "5d", "1wk", "1mo"],
        "max": ["1d", "5d", "1wk", "1mo"],
    }


def _safe_get(data: dict, key: str):
    """Return data[key] or 'N/A' if the key is missing (Yahoo's payload is inconsistent)."""
    return data.get(key, "N/A")


def fetch_stock_info(stock_ticker: str) -> dict:
    """Fetch and categorize the fundamental info for a given ticker."""
    raw = _ticker(stock_ticker).info

    return {
        "Basic Information": {
            "symbol": _safe_get(raw, "symbol"),
            "longName": _safe_get(raw, "longName"),
            "currency": _safe_get(raw, "currency"),
            "exchange": _safe_get(raw, "exchange"),
        },
        "Market Data": {
            "currentPrice": _safe_get(raw, "currentPrice"),
            "previousClose": _safe_get(raw, "previousClose"),
            "open": _safe_get(raw, "open"),
            "dayLow": _safe_get(raw, "dayLow"),
            "dayHigh": _safe_get(raw, "dayHigh"),
            "regularMarketPreviousClose": _safe_get(raw, "regularMarketPreviousClose"),
            "regularMarketOpen": _safe_get(raw, "regularMarketOpen"),
            "regularMarketDayLow": _safe_get(raw, "regularMarketDayLow"),
            "regularMarketDayHigh": _safe_get(raw, "regularMarketDayHigh"),
            "fiftyTwoWeekLow": _safe_get(raw, "fiftyTwoWeekLow"),
            "fiftyTwoWeekHigh": _safe_get(raw, "fiftyTwoWeekHigh"),
            "fiftyDayAverage": _safe_get(raw, "fiftyDayAverage"),
            "twoHundredDayAverage": _safe_get(raw, "twoHundredDayAverage"),
        },
        "Volume and Shares": {
            "volume": _safe_get(raw, "volume"),
            "regularMarketVolume": _safe_get(raw, "regularMarketVolume"),
            "averageVolume": _safe_get(raw, "averageVolume"),
            "averageVolume10days": _safe_get(raw, "averageVolume10days"),
            "averageDailyVolume10Day": _safe_get(raw, "averageDailyVolume10Day"),
            "sharesOutstanding": _safe_get(raw, "sharesOutstanding"),
            "impliedSharesOutstanding": _safe_get(raw, "impliedSharesOutstanding"),
            "floatShares": _safe_get(raw, "floatShares"),
        },
        "Dividends and Yield": {
            "dividendRate": _safe_get(raw, "dividendRate"),
            "dividendYield": _safe_get(raw, "dividendYield"),
            "payoutRatio": _safe_get(raw, "payoutRatio"),
        },
        "Valuation and Ratios": {
            "marketCap": _safe_get(raw, "marketCap"),
            "enterpriseValue": _safe_get(raw, "enterpriseValue"),
            "priceToBook": _safe_get(raw, "priceToBook"),
            "debtToEquity": _safe_get(raw, "debtToEquity"),
            "grossMargins": _safe_get(raw, "grossMargins"),
            "profitMargins": _safe_get(raw, "profitMargins"),
        },
        "Financial Performance": {
            "totalRevenue": _safe_get(raw, "totalRevenue"),
            "revenuePerShare": _safe_get(raw, "revenuePerShare"),
            "totalCash": _safe_get(raw, "totalCash"),
            "totalCashPerShare": _safe_get(raw, "totalCashPerShare"),
            "totalDebt": _safe_get(raw, "totalDebt"),
            "earningsGrowth": _safe_get(raw, "earningsGrowth"),
            "revenueGrowth": _safe_get(raw, "revenueGrowth"),
            "returnOnAssets": _safe_get(raw, "returnOnAssets"),
            "returnOnEquity": _safe_get(raw, "returnOnEquity"),
        },
        "Cash Flow": {
            "freeCashflow": _safe_get(raw, "freeCashflow"),
            "operatingCashflow": _safe_get(raw, "operatingCashflow"),
        },
        "Analyst Targets": {
            "targetHighPrice": _safe_get(raw, "targetHighPrice"),
            "targetLowPrice": _safe_get(raw, "targetLowPrice"),
            "targetMeanPrice": _safe_get(raw, "targetMeanPrice"),
            "targetMedianPrice": _safe_get(raw, "targetMedianPrice"),
        },
    }


def fetch_stock_history(stock_ticker: str, period: str, interval: str) -> pd.DataFrame:
    """Fetch OHLC candlestick data for a given ticker/period/interval."""
    stock_data = _ticker(stock_ticker)
    return stock_data.history(period=period, interval=interval)[
        ["Open", "High", "Low", "Close"]
    ]


def generate_stock_prediction(stock_ticker: str):
    """
    Fit an AutoReg (ARIMA-family) model on 2 years of daily closes and
    return (train, test, forecast, test_predictions).

    Returns (None, None, None, None) if anything goes wrong (e.g. ticker
    has too little history to fit a 250-lag model).
    """
    try:
        stock_data = _ticker(stock_ticker)
        hist = stock_data.history(period="2y", interval="1d")

        if hist.empty or len(hist) < 260:
            # Not enough history to fit a 250-lag AutoReg model reliably.
            return None, None, None, None

        close = hist[["Close"]].asfreq("D", method="ffill").ffill()

        split_idx = int(len(close) * 0.9) + 1
        train_df = close.iloc[:split_idx]
        test_df = close.iloc[split_idx - 1 :]

        model = AutoReg(train_df["Close"], lags=250).fit(cov_type="HC0")

        predictions = model.predict(
            start=test_df.index[0], end=test_df.index[-1], dynamic=True
        )
        forecast = model.predict(
            start=test_df.index[0],
            end=test_df.index[-1] + dt.timedelta(days=90),
            dynamic=True,
        )

        return train_df, test_df, forecast, predictions

    except Exception as exc:  # noqa: BLE001 - we want to surface this, not hide it
        print(f"[generate_stock_prediction] failed for {stock_ticker}: {exc}")
        return None, None, None, None
