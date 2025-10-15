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

# Real-time update loop
while True:
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")
        if not history.empty:
            price = history["Close"].iloc[-1]
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chart_data["times"].append(timestamp)
            st.session_state.chart_data["prices"].append(price)
            if len(st.session_state.chart_data["times"]) > 10:
                st.session_state.chart_data["times"].pop(0)
                st.session_state.chart_data["prices"].pop(0)
            chart.line_chart(st.session_state.chart_data["prices"])  # Update chart
            status.text(f"Last Price for {symbol}: {price} at {timestamp} UTC")
        else:
            status.text(f"No data for {symbol}")
    except Exception as e:
        status.text(f"Error: {e}")
    time.sleep(10)  # Update every 10 seconds