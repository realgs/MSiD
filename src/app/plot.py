import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app.config import MARKET_1, MARKET_2, END_TIME

def plot(df):
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x))

    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('Stock prices', 'Percentage change', 'Volume'))
    fig.add_trace(
        go.Candlestick(
            name='Stock prices',
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(
            name='Percentage change',
            x=df['time'],
            y=df['per_ch'],
        ),
        row=1, col=2,
    )
    fig.add_trace(
        go.Bar(
            name='Volume',
            x=df['time'],
            y=df['volume'],
        ),
        row=2, col=1,
    )

    # Add line separating predictions from real values
    line_date = END_TIME - timedelta(hours=12)
    fig.update_layout(title_text=f'{MARKET_1} {MARKET_2} predictions',
                      shapes = [dict(
                          x0=line_date, x1=line_date, y0=0, y1=1, xref='x', yref='paper', line_width=2,
                      )])

    fig.show()
