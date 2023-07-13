import plotly.graph_objects as go
def plot_candlestick_data(df):
    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
    fig.show()
  

def plot_candlestick_data_2(df):
    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
    fig.show()
  