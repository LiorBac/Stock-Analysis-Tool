import streamlit as st
import plotly.graph_objects as go

from stock_logic import get_stock_data
from visualizations import create_stock_chart

st.set_page_config(page_title="Stock Analysis Tool", layout="wide") # Set page configuration
st.title("📈 Stock Analysis Tool") #Set page title

with st.sidebar:
    st.header("Settings") # Sidebar header
    if st.button("Refresh Cache"): # Button to reset cache
        st.cache_data.clear() # Clear cached data
        st.rerun() # Success message
    ticker = st.text_input("Enter Stock Ticker", value="AAPL").upper() # Input for stock ticker
    st.info("Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL).") # Info message for ticker input
    period = st.selectbox("Select Data Period", options=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=2) # Select data period
    interval = st.selectbox("Select Data Interval", options=['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'], index=8) # Select data interval
    chart_type = st.selectbox("Select Chart Type", options=['Candlestick', 'Line'], index=0) # Select chart type


if ticker:
    hist, info = get_stock_data(ticker, period, interval) # Fetch stock data

    if hist.empty:
        st.error("No data found for the given ticker and parameters. Please check the ticker symbol and try again.") # Error message for no data
    else:
        company_name = info.get('longName', ticker) # Get company name or use ticker as fallback
        st.header(f"{company_name} ({ticker}) Stock Data") # Display company name and ticker

        if len(hist) >= 2: # Ensure there are at least 2 data points to calculate delta
            delta_val = hist['Close'].iloc[-1] - hist['Close'].iloc[-2] # Calculate price change
            delta_str = f"{delta_val:.2f} since last close" # Format delta string
        else:
            delta_str = "N/A" # Not enough data to calculate delta

        col1,col2,col3 = st.columns(3) # Create three columns for metrics
        col1.metric("Current Price", f"${hist['Close'].iloc[-1]:.2f}", delta_str) # Display current price with delta
        col2.metric("Highest today", f"${hist['High'].iloc[-1]:.2f}") # Display highest price today
        col3.metric("Lowest today", f"${hist['Low'].iloc[-1]:.2f}") # Display lowest price today

        st.markdown("---") # Horizontal separator

        st.subheader(f"Price Chart - {chart_type}") # Subheader for price chart
        fig = create_stock_chart(hist, company_name, ticker, chart_type) # Create stock chart
        
        st.plotly_chart(fig, width="stretch") # Display the chart

        with st.expander("Show Raw Data"): # Expander for raw data
            st.dataframe(hist.sort_index(ascending=False)) # Display raw historical data
            csv_data = hist.to_csv().encode('utf-8') # Convert data to CSV
            st.download_button(label="Download Data as CSV", data=csv_data, file_name=f"{ticker}_data.csv", mime='text/csv') # Download button for CSV data