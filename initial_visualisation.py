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
  
def plot_nasdaq(df,company,filename,covid):
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    
    #title
    if covid:
        fig.update_layout(
            annotations=[dict(
            x='2020-03-15', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='COVID-19 Crash Begins')],
            shapes = [dict(
            x0='2020-03-15', x1='2020-03-15', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
    
    )
            
    fig.update_layout(
        title=
        f"""Stock ticker:{company}\n 
            year: {filename}\n
            interval: daily \n
            chart type: Candlestick chart""",
            
        yaxis_title='Price'
    )
    
    
    fig.show()
    