import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Page config
st.set_page_config(page_title="📈 Real-Time Stock Dashboard", layout="wide")

# Dashboard title
st.title("📊 Real-Time Free Stock Dashboard")

# Input for multiple stock symbols
symbols_input = st.text_input("Enter stock symbols separated by comma (like AAPL, TSLA, INFY.NS):", "AAPL,TSLA")

refresh_rate = st.slider("Refresh every (seconds):", min_value=5, max_value=60, value=10, step=5)

if symbols_input:
    symbols = [s.strip().upper() for s in symbols_input.split(",")]

    st.subheader("Live Stock Data")
    placeholder = st.empty()  # Placeholder to update data dynamically

    while True:
        all_data = []
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                all_data.append({
                    "Symbol": info.get("symbol", "N/A"),
                    "Name": info.get("longName", "N/A"),
                    "Price": info.get("regularMarketPrice", "N/A"),
                    "Day High": info.get("dayHigh", "N/A"),
                    "Day Low": info.get("dayLow", "N/A"),
                    "Change": info.get("regularMarketChange", "N/A"),
                    "Change %": info.get("regularMarketChangePercent", "N/A")
                })
            except:
                all_data.append({
                    "Symbol": symbol,
                    "Name": "N/A",
                    "Price": "N/A",
                    "Day High": "N/A",
                    "Day Low": "N/A",
                    "Change": "N/A",
                    "Change %": "N/A"
                })

        df = pd.DataFrame(all_data)
        # Format Change % column to 2 decimals
        df["Change %"] = df["Change %"].apply(lambda x: round(x, 2) if isinstance(x, float) else x)

        # Display table dynamically
        placeholder.table(df)

        time.sleep(refresh_rate)
