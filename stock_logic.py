import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period='1mo', interval='1d'):
    # Fetch historical market data and stock info for a given ticker
    # Returns a tuple of (historical_data, stock_info)

    stock = yf.Ticker(ticker) # Create a Ticker object
    hist = stock.history(period=period, interval=interval) # Get historical market data
    
    try:
        info = stock.info # Get stock information
    except Exception:
        info = {}
    return hist, info