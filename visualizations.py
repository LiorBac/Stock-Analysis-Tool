import plotly.graph_objects as go
from stock_logic import calculate_normalized_prices

def create_stock_chart(hist, company_name, ticker, chart_type,benchmark_hist=None,benchmark_ticker=None):
    """Create a Plotly chart for stock data based on the specified chart type."""
    if benchmark_hist is not None:
        return create_benchmark_comparison_chart(hist, benchmark_hist, company_name, ticker, benchmark_ticker, chart_type) # Benchmark comparison chart
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

def create_benchmark_comparison_chart(hist, benchmark_hist, company_name, ticker, benchmark_name, chart_type):
    """Create a Plotly chart comparing stock data with a benchmark index."""
    # Normalize both datasets to start at 100
    normalized_hist = calculate_normalized_prices(hist)
    normalized_benchmark_hist = calculate_normalized_prices(benchmark_hist)

    # Create the chart
    fig = go.Figure()

    # Add stock data
    fig.add_trace(go.Scatter(
        x=normalized_hist.index, 
        y=normalized_hist, 
        mode='lines', 
        name=f'{company_name} ({ticker})',
        line=dict(color='#00C805', width=2)
    ))

    # Add benchmark data
    fig.add_trace(go.Scatter(
        x=normalized_benchmark_hist.index, 
        y=normalized_benchmark_hist, 
        mode='lines', 
        name=f'{benchmark_name}',
        line=dict(color='gray', width=2, dash='dash')
    ))

    # Update layout
    fig.update_layout(
        title=f"Performance Comparison: {ticker} vs {benchmark_name}",
        yaxis_title="Return (%)",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False,
        height=600,
        template="plotly_dark",
        yaxis=dict(tickformat=".1%")
    )
    return fig