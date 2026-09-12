import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="FinTech Market Simulator", page_icon="📈", layout="wide")

st.title("📈 Algorithmic Stock Market Analytics Simulator")
st.write("Fetch real-time historical financial market data and isolate equity price trends using mathematical indicators.")

# 2. Sidebar Controls
st.sidebar.header("Market Parameters")
ticker = st.sidebar.text_input("Enter Equity Ticker (e.g., AAPL, GOOG, MSFT, BTC-USD):", "AAPL")
days = st.sidebar.slider("Historical Data Range (Days):", 30, 365, 180)
window_size = st.sidebar.slider("Algorithmic Rolling Window (SMA Days):", 5, 50, 20)

# 3. Data Processing & Visualization Engine
if ticker:
    try:
        with st.spinner(f"Streaming data metrics for {ticker.upper()}..."):
            # Fetch historical market data from yfinance API
            stock_data = yf.download(ticker, period=f"{days}d")
        
        if not stock_data.empty:
            # Drop multi-level index columns if present to clean data architecture
            if isinstance(stock_data.columns, pd.MultiIndex):
                stock_data.columns = stock_data.columns.get_level_values(0)
            
            # Calculate a Simple Moving Average (SMA) using Pandas rolling windows
            stock_data['SMA_Indicator'] = stock_data['Close'].rolling(window=window_size).mean()
            
            # 4. Render Visual Analytics Charts
            st.subheader(f"📊 Quantitative Price Trend Analysis: {ticker.upper()}")
            
            # Align charting data structures
            chart_df = pd.DataFrame({
                'Market Close ($)': stock_data['Close'],
                f'{window_size}-Day SMA Line': stock_data['SMA_Indicator']
            }, index=stock_data.index)
            
            st.line_chart(chart_df)
            
            # 5. Display Structured Statistical Tables
            st.subheader("📋 Core Data Analytics Log")
            st.dataframe(stock_data[['Open', 'High', 'Low', 'Close', 'Volume']].tail(5), use_container_width=True)
            
        else:
            st.error("Data pipeline empty. Please verify equity ticker configuration.")
            
    except Exception as e:
        st.error(f"Data Engine Error: {e}")
