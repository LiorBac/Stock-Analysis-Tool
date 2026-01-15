# 📈 Stock Analysis Tool

A web-based application built with **Python** and **Streamlit** for real-time stock market analysis. The tool allows users to visualize stock data and compare performance against major market benchmarks.

## 🚀 Features

* **Real-time Data:** Fetches up-to-date stock data using Yahoo Finance API.
* **Interactive Visualizations:**
    * Candlestick and Line charts using Plotly.
    * Dynamic Zoom & Pan.
* **Benchmark Comparison:** Compare any stock's performance against major indices (S&P 500, NASDAQ, Dow Jones) with normalized percentage return.
* **Flexible Timeframes:** Choose pre-defined periods (1Y, YTD, etc.) or select custom date ranges.
* **Data Export:** Download historical data as CSV.
* **Performance:** Implemented caching for fast loading times.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Frontend:** Streamlit
* **Data Source:** yfinance
* **Visualization:** Plotly
* **Data Manipulation:** Pandas

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/LiorBac/Stock-Analysis-Tool.git](https://github.com/LiorBac/Stock-Analysis-Tool.git)
    cd Stock-Analysis-Tool
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📸 Usage

1.  Enter a stock ticker (e.g., `AAPL`, `NVDA`, `TSLA`) in the sidebar.
2.  Select your desired time period or custom dates.
3.  Choose a chart type (Candlestick/Line).
4.  (Optional) Select a benchmark to compare performance.

## 🔮 Future Improvements

* Integration of RSI and MACD indicators.
* Backtesting engine for trading strategies.
* Reinforcement Learning agent for automated trading analysis.

---
*Built as part of a portfolio project.*