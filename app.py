import streamlit as st
import datetime
import matplotlib.pyplot as plt
from psx import stocks
import sys
import os

# Add the 'src' folder to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


# --- Page Config ---
st.set_page_config(page_title="PSX Stock Viewer", layout="centered")
st.title("📈 Pakistan Stock Exchange (PSX) Data Viewer")
st.markdown("Enter a stock symbol (e.g. `SILK`, `MCB`, `JSBL`) and select a date range to view historical data.")

# --- Input Widgets ---
ticker = st.text_input("Enter PSX Ticker Symbol", "SILK").upper()

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.date(2020, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime.date.today())

# --- Fetch Data ---
if st.button("Fetch Data"):
    try:
        data = stocks(ticker, start=start_date, end=end_date)

        if data.empty:
            st.warning("No data returned. Please check the ticker symbol or date range.")
        else:
            st.success(f"Data for {ticker} loaded successfully!")

            # Show data table
            st.dataframe(data.tail())

            # Plot Close price
            if "Close" in data.columns:
                st.line_chart(data["Close"])
            else:
                st.warning("No 'Close' column found in the data to plot.")
    except Exception as e:
        st.error(f"⚠️ An error occurred:\n\n{e}")
