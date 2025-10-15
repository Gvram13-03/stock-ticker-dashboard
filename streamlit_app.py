import streamlit as st
import yfinance as yf
from datetime import datetime, timezone
import time

st.title("Live Stock Ticker Dashboard")

# Sidebar for stock selection
symbol = st.sidebar.selectbox("Select Stock", ["MSFT", "AAPL", "GOOGL"], index=0)

# Initialize session state for chart data
if "chart_data" not in st.session_state:
    st.session_state.chart_data = {"times": [], "prices": []}

# Chart setup
chart = st.line_chart(st.session_state.chart_data["prices"], width=600, height=400)
status = st.empty()

# Real-time update loop with retries
def fetch_price(symbol):
    for period in ["1d", "5d", "1mo"]:
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period)
            if not history.empty:
                return history["Close"].iloc[-1], datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            continue
    return None, None

while True:
    price, timestamp = fetch_price(symbol)
    if price is not None:
        st.session_state.chart_data["times"].append(timestamp)
        st.session_state.chart_data["prices"].append(price)
        if len(st.session_state.chart_data["times"]) > 10:
            st.session_state.chart_data["times"].pop(0)
            st.session_state.chart_data["prices"].pop(0)
        chart.line_chart(st.session_state.chart_data["prices"])
        status.text(f"Last Price for {symbol}: {price} at {timestamp} UTC")
    else:
        status.text(f"Connection error or no data for {symbol}")
    time.sleep(10)