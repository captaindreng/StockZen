"""
pages/02_Stock_Prediction.py
-----------------------------
Plots historical candlestick data and an ARIMA-based (AutoReg) forecast.
"""

import plotly.graph_objects as go
import streamlit as st

from helper import (
    fetch_stocks,
    fetch_periods_intervals,
    fetch_stock_history,
    generate_stock_prediction,
)

st.set_page_config(page_title="Stock Price Prediction", page_icon="📈")

# ----- Sidebar -----
st.sidebar.markdown("## User Input Features")

stock_dict = fetch_stocks()
stock = st.sidebar.selectbox("Choose a stock", list(stock_dict.keys()))
stock_exchange = st.sidebar.radio("Choose a stock exchange", ("BSE", "NSE"), index=0)
stock_ticker = f"{stock_dict[stock]}.{'BO' if stock_exchange == 'BSE' else 'NS'}"
st.sidebar.text_input("Stock ticker code", value=stock_ticker, disabled=True)

periods = fetch_periods_intervals()
period = st.sidebar.selectbox("Choose a period", list(periods.keys()), index=5)  # default "1y"
interval = st.sidebar.selectbox("Choose an interval", periods[period])

# ----- Title -----
st.markdown("# Stock Price Prediction")
st.markdown("##### Enhance Investment Decisions through Data-Driven Forecasting")

# ----- Historical Data -----
st.markdown("## Historical Data")

stock_data = fetch_stock_history(stock_ticker, period, interval)

if stock_data.empty:
    st.warning("No historical data available for this ticker/period/interval combination.")
else:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
            )
        ]
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# ----- Prediction -----
st.markdown("## Stock Prediction")

train_df, test_df, forecast, predictions = generate_stock_prediction(stock_ticker)

if train_df is not None:
    fig = go.Figure(
        data=[
            go.Scatter(x=train_df.index, y=train_df["Close"], name="Train", line=dict(color="blue")),
            go.Scatter(x=test_df.index, y=test_df["Close"], name="Test", line=dict(color="orange")),
            go.Scatter(x=forecast.index, y=forecast, name="Forecast", line=dict(color="red")),
            go.Scatter(x=test_df.index, y=predictions, name="Test Predictions", line=dict(color="green")),
        ]
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(
        "Not enough historical data to generate a reliable forecast for this stock "
        "(AutoReg needs ~1 year+ of daily data)."
    )
