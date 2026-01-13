import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data(ttl=24*3600)
def get_stock_data(ticker, period='1mo', interval='1d'):
    # Fetch historical market data and stock info for a given ticker
    # Returns a tuple of (historical_data, stock_info)

    stock = yf.Ticker(ticker) # Create a Ticker object
    hist = stock.history(period=period, interval=interval, auto_adjust=True) # Get historical data
    
    try:
        info = stock.info # Get stock information
    except Exception:
        info = {}
    return hist, info