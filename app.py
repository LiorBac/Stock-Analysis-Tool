import streamlit as st
import plotly.graph_objects as go

from stock_logic import get_stock_data

st.set_page_config(page_title="Stock Analysis Tool", layout="wide") # Set page configuration
st.title("📈 Stock Analysis Tool") #Set page title

with st.sidebar:
    st.header("Settings") # Sidebar header
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
        if chart_type == "Candlestick": # Candlestick chart
            fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                                 open=hist['Open'],high=hist['High'],low=hist['Low'],close=hist['Close'],name='Price')]) # Create candlestick chart
        else:
            start_price = hist['Close'].iloc[0] # Get starting price
            end_price = hist['Close'].iloc[-1] # Get ending price
            if end_price > start_price: # Determine color based on price movement
                line_color = 'green'
                fill_color = 'rgba(0, 200, 5, 0.2)' # Green shade for increase
            else:
                line_color = 'red'
                fill_color = 'rgba(255, 51, 51, 0.2)' # Red shade for decrease

            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines',name='Close Price', line=dict(color=line_color,width=2), fill='tozeroy', fillcolor=fill_color)]) # Create line chart with dynamic coloring
        
        fig.update_layout(title=f"{company_name} ({ticker}) Price Chart",
                          yaxis_title="Price (USD)",
                          xaxis_title="Date",
                          xaxis_rangeslider_visible=False,
                          height=600,
                          template="plotly_dark") # Update chart layout
        
        st.plotly_chart(fig, width="stretch") # Display the chart

        with st.expander("Show Raw Data"): # Expander for raw data
            st.dataframe(hist.sort_index(ascending=False)) # Display raw historical data