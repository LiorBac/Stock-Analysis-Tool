import plotly.graph_objects as go

def create_stock_chart(hist, company_name, ticker, chart_type):
    """Create a Plotly chart for stock data based on the specified chart type."""
    if chart_type == "Candlestick":
        fig = create_stock_candlestick_chart(hist) # Candlestick chart
    else:
        fig = create_stock_scatter_chart(hist) # Line chart
    
    
    fig = _apply_chart_layout(fig, hist, company_name, ticker) # Apply common layout
    return fig

def create_stock_scatter_chart(hist): 
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
    return fig

def create_stock_candlestick_chart(hist):
    """Create a Plotly candlestick chart for stock prices."""
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                         open=hist['Open'], high=hist['High'],
                                         low=hist['Low'], close=hist['Close'],
                                         name='Price')])
    return fig

def _apply_chart_layout(fig, hist, company_name, ticker):
    """Apply common layout settings to the chart."""
    # Set y-axis limits with padding
    y_min = hist['Low'].min()
    y_max = hist['High'].max()
    padding = (y_max - y_min) * 0.05
    ylim_low = y_min - padding
    ylim_high = y_max + padding

    # Update layout
    fig.update_layout(title=f"{company_name} ({ticker}) Price Chart",
                      yaxis_title="Price (USD)",
                      xaxis_title="Date",
                      xaxis_rangeslider_visible=False,
                      height=600,
                      template="plotly_dark",
                    yaxis=dict(range=[ylim_low, ylim_high]))
    return fig