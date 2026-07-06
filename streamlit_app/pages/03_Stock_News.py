"""
pages/03_Stock_News.py
------------------------
Shows recent news headlines for a ticker. Tries Yahoo Finance's
unofficial news endpoint first, falls back to the Finnhub API.

IMPORTANT: the Finnhub API key is read from Streamlit secrets
(`st.secrets["FINNHUB_API_KEY"]`) — never hardcode API keys in source code,
since the repo (and key) become public the moment you push to GitHub.

Local setup: create `.streamlit/secrets.toml` with:
    FINNHUB_API_KEY = "your_key_here"

Streamlit Community Cloud setup: paste the same line into
App settings -> Secrets in the dashboard.
"""

from datetime import datetime, timedelta

import requests
import streamlit as st

st.set_page_config(page_title="Live Stock News", page_icon="📰", layout="wide")

FINNHUB_API_KEY = st.secrets.get("FINNHUB_API_KEY", "")


@st.cache_data(ttl=3600)
def fetch_yahoo_news(ticker: str):
    """Attempt to fetch news from Yahoo Finance's unofficial API."""
    url = f"https://query2.finance.yahoo.com/v6/finance/news?symbols={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            news = resp.json()
            if isinstance(news, dict):
                return news.get("items") or news.get("news") or []
    except requests.RequestException:
        pass
    return None


@st.cache_data(ttl=3600)
def fetch_finnhub_news(ticker: str, api_key: str):
    """Fetch company news from Finnhub (fallback source)."""
    if not api_key:
        return []
    today = datetime.utcnow().date()
    last_week = today - timedelta(days=7)
    url = (
        "https://finnhub.io/api/v1/company-news"
        f"?symbol={ticker}&from={last_week}&to={today}&token={api_key}"
    )
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except requests.RequestException:
        pass
    return []


def format_unix_timestamp(ts) -> str:
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %I:%M %p")
    except (ValueError, TypeError):
        return str(ts)


# ----- UI -----
st.title("📊 Live Financial News")

st.sidebar.header("Stock Ticker")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()

st.sidebar.markdown("---")
st.sidebar.write("News is fetched from Yahoo Finance when available, otherwise Finnhub (fallback).")

if not FINNHUB_API_KEY:
    st.sidebar.warning("No Finnhub API key configured — fallback news source will be unavailable.")

st.subheader(f"Live News for {ticker}")

news_data = fetch_yahoo_news(ticker)

if not news_data:
    st.warning("Yahoo news unavailable or blocked. Falling back to Finnhub.")
    news_items = fetch_finnhub_news(ticker, FINNHUB_API_KEY)
    source = "Finnhub"
else:
    news_items = news_data
    source = "Yahoo"

if news_items:
    for item in news_items:
        title = item.get("title") or item.get("headline") or "No Title Available"
        link = item.get("link") or item.get("url")
        publisher = item.get("publisher") or item.get("source", "Unknown Publisher")
        ts = item.get("providerPublishTime") or item.get("datetime")
        published = format_unix_timestamp(ts) if ts else "N/A"

        st.markdown(f"### {title}")
        st.write(f"**Publisher:** {publisher}")
        st.write(f"**Published:** {published}")
        if link:
            st.write(f"[Read more]({link})")
        st.markdown("---")
else:
    st.info(f"No news articles found via {source}.")
