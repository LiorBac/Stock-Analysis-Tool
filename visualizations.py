import plotly.graph_objects as go

def create_stock_chart(hist, company_name, ticker, chart_type):
    """Create a Plotly chart for stock data based on the specified chart type."""
    if chart_type == "Candlestick":
        return create_stock_candlestick_chart(hist, company_name, ticker) # Candlestick chart
    else:
        return create_stock_scatter_chart(hist, company_name, ticker) # Line chart

def create_stock_scatter_chart(hist, company_name, ticker): 
    """Create a Plotly scatter chart for stock closing prices."""
    start_price = hist['Close'].iloc[0]
    end_price = hist['Close'].iloc[-1]
    if end_price > start_price:
        line_color = 'green'
        fill_color = 'rgba(0, 200, 5, 0.2)'  # Green shade for increase
    else:
        line_color = 'red'
        fill_color = 'rgba(255, 51, 51, 0.2)'  # Red shade for decrease

    fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'],
                                     mode='lines', name='Close Price',
                                     line=dict(color=line_color, width=2),
                                     fill='tozeroy', fillcolor=fill_color)])

    fig.update_layout(title=f"{company_name} ({ticker}) Price Chart",
                      yaxis_title="Price (USD)",
                      xaxis_title="Date",
                      xaxis_rangeslider_visible=False,
                      height=600,
                      template="plotly_dark")
    return fig

def create_stock_candlestick_chart(hist, company_name, ticker):
    """Create a Plotly candlestick chart for stock prices."""
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                         open=hist['Open'], high=hist['High'],
                                         low=hist['Low'], close=hist['Close'],
                                         name='Price')])

    fig.update_layout(title=f"{company_name} ({ticker}) Price Chart",
                      yaxis_title="Price (USD)",
                      xaxis_title="Date",
                      xaxis_rangeslider_visible=False,
                      height=600,
                      template="plotly_dark")
    return fig