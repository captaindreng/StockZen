"""
Main.py
-------
Landing page for StockZen. Streamlit auto-discovers files in the
`pages/` folder and adds them as extra pages in the sidebar nav.
"""

import streamlit as st

st.set_page_config(
    page_title="StockZen",
    page_icon="📈",
    layout="centered",
)

st.markdown(
    """
# 📈 StockZen

### Predicting Stocks with ML

StockZen is an ML-powered stock price prediction app built with Python and
Streamlit. It pulls live market data and forecasts future prices using a
time-series model, so you can explore trends without risking real money.

## How it works

1. Pick a stock (BSE or NSE listed) from the sidebar on any page
2. **Stock Info** — pulls live fundamentals & valuation data via yfinance
3. **Stock Prediction** — fits an AutoReg (ARIMA-family) model on 2 years of
   daily closes and forecasts 90 days ahead
4. **Stock News** — pulls the latest headlines for that ticker

## Tech stack

- **Streamlit** – UI and page routing
- **yfinance** – live + historical market data from Yahoo Finance
- **statsmodels** – AutoReg time-series forecasting
- **plotly** – interactive candlestick & forecast charts

---

⚖️ **Disclaimer:** This is not financial advice. Forecasts are for
educational purposes only — there's no guarantee of trading performance.
Use them to inform your own research, not as a substitute for it.
"""
)
