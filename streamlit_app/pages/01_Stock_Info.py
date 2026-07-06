"""
pages/01_Stock_Info.py
-----------------------
Shows fundamental & valuation data for a chosen stock.

The original version of this page repeated the same
`st.dataframe(pd.DataFrame({...}))` pattern ~40 times. Here it's collapsed
into a small `show_row()` helper so the page is readable and easy to extend.
"""

import pandas as pd
import streamlit as st

from helper import fetch_stocks, fetch_stock_info

st.set_page_config(page_title="Stock Info", page_icon="🏛️")

# ----- Sidebar -----
st.sidebar.markdown("## User Input Features")

stock_dict = fetch_stocks()
stock = st.sidebar.selectbox("Choose a stock", list(stock_dict.keys()))
stock_exchange = st.sidebar.radio("Choose a stock exchange", ("BSE", "NSE"), index=0)
stock_ticker = f"{stock_dict[stock]}.{'BO' if stock_exchange == 'BSE' else 'NS'}"

st.sidebar.text_input("Stock ticker code", value=stock_ticker, disabled=True)

# ----- Fetch data -----
try:
    info = fetch_stock_info(stock_ticker)
except Exception:
    st.error("Unable to fetch data for this ticker. Please try another stock.")
    st.stop()


def show_row(section: str, *fields: tuple[str, str]):
    """Render one or more fields from `info[section]` side by side as columns.

    Each field is a (label, key) tuple, e.g. ("Current Price", "currentPrice").
    """
    cols = st.columns(len(fields))
    for col, (label, key) in zip(cols, fields):
        col.dataframe(pd.DataFrame({label: [info[section][key]]}), hide_index=True)


# ----- Title -----
st.markdown("# Stock Info")
st.markdown("##### Enhancing Your Stock Market Insights")

# ----- Basic Information -----
st.markdown("## Basic Information")
show_row("Basic Information", ("Issuer Name", "longName"), ("Currency", "currency"))
st.dataframe(pd.DataFrame({"Symbol": [stock_ticker]}), hide_index=True)

# ----- Market Data -----
st.markdown("## Market Data")
show_row("Market Data", ("Current Price", "currentPrice"), ("Previous Close", "previousClose"))
show_row("Market Data", ("Open", "open"), ("Day Low", "dayLow"), ("Day High", "dayHigh"))
show_row(
    "Market Data",
    ("52-Week Low", "fiftyTwoWeekLow"),
    ("52-Week High", "fiftyTwoWeekHigh"),
    ("50-Day Average", "fiftyDayAverage"),
)

# ----- Volume and Shares -----
st.markdown("## Volume and Shares")
show_row("Volume and Shares", ("Volume", "volume"), ("Regular Market Volume", "regularMarketVolume"))
show_row(
    "Volume and Shares",
    ("Average Volume", "averageVolume"),
    ("Shares Outstanding", "sharesOutstanding"),
    ("Float Shares", "floatShares"),
)

# ----- Dividends and Yield -----
st.markdown("## Dividends and Yield")
show_row(
    "Dividends and Yield",
    ("Dividend Rate", "dividendRate"),
    ("Dividend Yield", "dividendYield"),
    ("Payout Ratio", "payoutRatio"),
)

# ----- Valuation and Ratios -----
st.markdown("## Valuation and Ratios")
show_row("Valuation and Ratios", ("Market Cap", "marketCap"), ("Enterprise Value", "enterpriseValue"))
show_row("Valuation and Ratios", ("Price to Book", "priceToBook"), ("Debt to Equity", "debtToEquity"))
show_row("Valuation and Ratios", ("Gross Margins", "grossMargins"), ("Profit Margins", "profitMargins"))

# ----- Financial Performance -----
st.markdown("## Financial Performance")
show_row("Financial Performance", ("Total Revenue", "totalRevenue"), ("Revenue Per Share", "revenuePerShare"))
show_row("Financial Performance", ("Earnings Growth", "earningsGrowth"), ("Revenue Growth", "revenueGrowth"))
show_row("Financial Performance", ("Return on Assets", "returnOnAssets"), ("Return on Equity", "returnOnEquity"))

# ----- Cash Flow -----
st.markdown("## Cash Flow")
show_row("Cash Flow", ("Free Cash Flow", "freeCashflow"), ("Operating Cash Flow", "operatingCashflow"))

# ----- Analyst Targets -----
st.markdown("## Analyst Targets")
show_row("Analyst Targets", ("Target High", "targetHighPrice"), ("Target Low", "targetLowPrice"))
show_row("Analyst Targets", ("Target Mean", "targetMeanPrice"), ("Target Median", "targetMedianPrice"))
