import streamlit as st
import datetime
import os
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Ensure local package access
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from psx import stocks

# --- Page Setup ---
st.set_page_config(page_title="📊 PSX Stock Dashboard", layout="wide")
st.title("📈 Pakistan Stock Exchange - Full Stock Chart Dashboard")

# --- Input Section ---
with st.form("input_form"):
    ticker = st.text_input("Enter PSX Ticker Symbol", "SILK").upper()
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.date(2020, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime.date.today())
    submit_btn = st.form_submit_button("Load Stock Charts")

# --- Load Data and Visualize ---
if submit_btn:
    try:
        df = stocks(ticker, start=start_date, end=end_date)

        if df.empty:
            st.warning("⚠️ No data returned. Please check the ticker and date range.")
        else:
            st.success(f"✅ Data for {ticker} loaded with {len(df)} records.")

            # --- Show Latest Records ---
            st.subheader("📄 Latest Records")
            st.dataframe(df.tail(10))

            # --- Full Data Table ---
            with st.expander("📊 Full Data View"):
                st.dataframe(df)
                csv = df.to_csv().encode('utf-8')
                st.download_button("Download CSV", csv, f"{ticker}_psx_data.csv", "text/csv")

            # --- 1. Close Price Line Chart ---
            st.subheader("1️⃣ Close Price Over Time")
            st.line_chart(df["Close"])

            # --- 2. Volume Bar Chart ---
            st.subheader("2️⃣ Volume Over Time")
            st.bar_chart(df["Volume"])

            # --- 3. Full Candlestick + Volume Chart ---
            st.subheader("3️⃣ Full Historical Candlestick Chart")
            fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                 vertical_spacing=0.1, row_width=[0.2, 0.8],
                                 subplot_titles=(f"{ticker} Price", "Volume"))

            fig1.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                increasing_line_color='green',
                decreasing_line_color='red',
                name="Price"
            ), row=1, col=1)

            fig1.add_trace(go.Bar(
                x=df.index,
                y=df["Volume"],
                marker_color='lightblue',
                name="Volume"
            ), row=2, col=1)

            fig1.update_layout(height=700, width=1400, showlegend=False,
                               xaxis_rangeslider_visible=False)
            st.plotly_chart(fig1, use_container_width=True)

            # --- 4. Zoomed-In Candlestick (6 months) ---
            st.subheader("4️⃣ Zoomed-In Candlestick Chart (Last 6 Months)")
            if len(df) >= 1:
                zoom_df = df[df.index >= (df.index.max() - datetime.timedelta(days=180))]

                fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                     vertical_spacing=0.1, row_width=[0.2, 0.8],
                                     subplot_titles=(f"{ticker} (Last 6 Months)", "Volume"))

                fig2.add_trace(go.Candlestick(
                    x=zoom_df.index,
                    open=zoom_df["Open"],
                    high=zoom_df["High"],
                    low=zoom_df["Low"],
                    close=zoom_df["Close"],
                    increasing_line_color='green',
                    decreasing_line_color='red',
                    name="Price"
                ), row=1, col=1)

                fig2.add_trace(go.Bar(
                    x=zoom_df.index,
                    y=zoom_df["Volume"],
                    marker_color='lightgreen',
                    name="Volume"
                ), row=2, col=1)

                fig2.update_layout(height=700, width=1400, showlegend=False,
                                   xaxis_rangeslider_visible=False)
                st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error occurred:\n\n{e}")
