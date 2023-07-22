import pandas as pd
import numpy as np
from matplotlib import pyplot
import plotly.graph_objects as go


def trendline_detect(file:str):
    """
    This function detects trendlines in a given financial dataset and plots them using Plotly.

    Args:
    file (str): The file path of the financial dataset.

    Returns:
    None
    """
    # Read the financial dataset
    df = pd.read_csv("EURUSD_Candlestick_4_Hour_ASK_05.05.2003-16.10.2021 (1).csv")

    # Rename the columns of the dataset
    df.columns=['time', 'open', 'high', 'low', 'close', 'volume']

    # Remove rows with NA values
    df=df[df['volume']!=0]

    # Reset the index of the dataset
    df.reset_index(drop=True, inplace=True)

    # Print the first 10 rows of the dataset
    df.head(10)

    backcandles= 70
    brange = 50 #should be less than backcandles
    wind = 5

    candleid = 150
    dfpl = df[:2000]
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                        open=dfpl['open'],
                        high=dfpl['high'],
                        low=dfpl['low'],
                        close=dfpl['close'])])
    
    while candleid < 2000:

        optbackcandles= backcandles
        sldiff = 100
        sldist = 10000
        for r1 in range(backcandles-brange, backcandles+brange):
            maxim = np.array([])
            minim = np.array([])
            xxmin = np.array([])
            xxmax = np.array([])
            
            for i in range(candleid-r1, candleid+1, wind):
                minim = np.append(minim, df.low.iloc[i:i+wind].min())
                xxmin = np.append(xxmin, df.low.iloc[i:i+wind].idxmin())
            for i in range(candleid-r1, candleid+1, wind):
                maxim = np.append(maxim, df.high.loc[i:i+wind].max())
                xxmax = np.append(xxmax, df.high.iloc[i:i+wind].idxmax())
            slmin, intercmin = np.polyfit(xxmin, minim,1)
            slmax, intercmax = np.polyfit(xxmax, maxim,1)
            
            dist = (slmax*candleid + intercmax)-(slmin*candleid + intercmin)
            if(dist<sldist): #abs(slmin-slmax)<sldiff and
                #sldiff = abs(slmin-slmax)
                sldist = dist
                optbackcandles=r1
                slminopt = slmin
                slmaxopt = slmax
                intercminopt = intercmin
                intercmaxopt = intercmax
                maximopt = maxim.copy()
                minimopt = minim.copy()
                xxminopt = xxmin.copy()
                xxmaxopt = xxmax.copy()

                
        
        dfpl = df[candleid-wind-optbackcandles-backcandles:candleid+optbackcandles]  
        

        adjintercmax = (df.high.iloc[xxmaxopt] - slmaxopt*xxmaxopt).max()
        adjintercmin = (df.low.iloc[xxminopt] - slminopt*xxminopt).min()
        fig.add_trace(go.Scatter(x=xxminopt, y=slminopt*xxminopt + adjintercmin, mode='lines', name='min slope', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=xxmaxopt, y=slmaxopt*xxmaxopt + adjintercmax, mode='lines', name='max slope', line=dict(color='green')))
        candleid += optbackcandles
        
        
    fig.show()

trendline_detect("EURUSD_Candlestick_4_Hour_ASK_05.05.2003-16.10.2021.csv")