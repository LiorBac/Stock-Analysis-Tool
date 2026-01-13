import streamlit as st
import plotly.graph_objects as go

from stock_logic import get_stock_data

st.set_page_config(page_title="Stock Analysis Tool", layout="wide") # Set page configuration
st.title("📈 Stock Analysis Tool") #Set page title

with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Enter Stock Ticker", value="AAPL").upper() # Input for stock ticker
    st.info("Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL).")
    period = st.selectbox("Select Data Period", options=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=2) # Select data period
    interval = st.selectbox("Select Data Interval", options=['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'], index=8) # Select data interval
    chat_type = st.selectbox("Select Chart Type", options=['Candlestick', 'Line'], index=0) # Select chart type

if ticker:
    hist, info = get_stock_data(ticker, period, interval) # Fetch stock data

    if hist.empty:
        st.error("No data found for the given ticker and parameters. Please check the ticker symbol and try again.")
    else:
        company_name = info.get('longName', ticker)
        st.header(f"{company_name} ({ticker}) Stock Data")

        col1,col2,col3 = st.columns(3)
        col1.metric("Current Price", f"${hist['Close'][-1]:.2f}", f"{hist['Close'][-1] - hist['Close'][-2]:.2f} since last close")
        col2.metric("Highest today", f"${hist['High'][-1]:.2f}")
        col3.metric("Lowest today", f"${hist['Low'][-1]:.2f}")

        st.markdown("---")

        st.subheader(f"Price Chart - {chat_type}")
        if chat_type == "Candlestick":
            fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                                 open=hist['Open'],high=hist['High'],low=hist['Low'],close=hist['Close'],name='Price')])
        else:
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            if end_price > start_price:
                line_color = 'green'
                fill_color = 'rgba(0, 200, 5, 0.2)'
            else:
                line_color = 'red'
                fill_color = 'rgba(255, 51, 51, 0.2)' 

            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines',name='Close Price', line=dict(color=line_color,width=2), fill='tozeroy', fillcolor=fill_color)])
        
        fig.update_layout(title=f"{company_name} ({ticker}) Price Chart",
                          yaxis_title="Price (USD)",
                          xaxis_title="Date",
                          xaxis_rangeslider_visible=False)
        
        fig.update_layout(height=600,template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show Raw Data"):
            st.dataframe(hist.sort_index(ascending=False))