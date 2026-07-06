# 📈 StockZen

ML-powered stock price prediction app built with Python and Streamlit.
Fetches live market data, shows fundamentals, and forecasts future prices
using a time-series model — built as a learning project, not financial advice.

## Features

- **Stock Info** — live fundamentals, valuation, dividends, and analyst targets for any BSE/NSE-listed stock
- **Stock Prediction** — candlestick chart of historical prices + a 90-day AutoReg (ARIMA-family) forecast
- **Stock News** — recent headlines per ticker (Yahoo Finance, falls back to Finnhub)

## Tech stack

| Purpose | Library |
|---|---|
| Web UI | Streamlit |
| Market data | yfinance |
| Forecasting | statsmodels (AutoReg) |
| Charts | Plotly |

## Project structure

```
StockZen/
├── streamlit_app/
│   ├── Main.py                  # landing page
│   ├── helper.py                 # shared data-fetching logic
│   └── pages/
│       ├── 01_Stock_Info.py
│       ├── 02_Stock_Prediction.py
│       └── 03_Stock_News.py
├── data/
│   └── equity_issuers.csv        # BSE-listed company reference list
├── .streamlit/
│   ├── config.toml               # theme
│   └── secrets.toml.example      # copy to secrets.toml, fill in your key
├── requirements.txt
└── README.md
```

## Running locally

```bash
git clone https://github.com/<your-username>/StockZen.git
cd StockZen
pip install -r requirements.txt

# Set up your API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste your real Finnhub key

streamlit run streamlit_app/Main.py
```

App runs at `http://localhost:8501`.

Get a free Finnhub API key at https://finnhub.io/register (only needed as a
fallback for the news page).

## Deploying (Streamlit Community Cloud)

1. Push this repo to your own GitHub account
2. Go to https://share.streamlit.io → "New app"
3. Pick your repo, set **Main file path** to `streamlit_app/Main.py`
4. In **Advanced settings → Secrets**, paste:
   ```
   FINNHUB_API_KEY = "your_real_key"
   ```
5. Deploy — you'll get a public `*.streamlit.app` URL

## Roadmap

- LSTM-based forecasting as an alternative model
- Portfolio tracking across multiple holdings
- User accounts / watchlists

## Disclaimer

This is **not financial advice**. Forecasts are for educational purposes
only — there is no guarantee of trading performance.
