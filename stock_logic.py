import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data(ttl=24*3600)
def get_stock_data(ticker, period='1mo', interval='1d',start=None,end=None):
    # Fetch historical market data and stock info for a given ticker
    # Returns a tuple of (historical_data, stock_info)
    try:
        stock = yf.Ticker(ticker) # Create a Ticker object
        if start is None and end is None:
            hist = stock.history(period=period, interval=interval, auto_adjust=True) # Get historical data
        else:
            if end == start:
                end = None
            else:
                hist= stock.history(start=start, end=end, interval=interval, auto_adjust=True) # Get historical data for custom dates
        
        try:
            info = stock.info # Get stock information
        except:
            info = {}
        return hist, info
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame(), {}
    

def calculate_normalized_prices(hist):
    # Calculate normalized closing prices relative to the starting price
    if hist.empty:
        return hist
    
    start_price = hist['Close'].iloc[0] # Get the starting closing price
    return (hist['Close'] / start_price) - 1 # Normalize prices