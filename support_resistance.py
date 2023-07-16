import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

def detection_support_resistance(file:str):
    #file is a csv file
    df = pd.read_csv(file)
    df = pd.DataFrame(df, columns=['Date', 'Close/Last', 'Volume', 'Open', 'High', 'Low'])
    dats = df['Date']
    dats = dats[::-1]
    # Format the Date column as datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df.set_index('Date', inplace=True)
    #sort the data by date
    df.sort_values("Date", inplace=True)
    # Rename the column for compatibility with plot_candlestick_data function
   
    
    #check when the volume is 0 = no trading
    df = df[df['Volume'] != 0]
    
    # Replace "$" with an empty string in multiple columns
    columns_to_replace = ['Close/Last', 'Open', 'High', 'Low']
    df[columns_to_replace] = df[columns_to_replace].applymap(lambda x: x.replace('$', ''))

    

    
    def support(df1, l, n1, n2)->1 or 0:
        #df1 is the dataframe
        #l is the row
        #n1 is the number of candles before
        #n2 is the number of candles after
        
        for i in range(l-n1+1, l+1):
            #if the low of the candle is higher than the low of the previous candle
            if(df1.Low[i]>df1.Low[i-1]):
                return 0
            
        
        for i in range(l+1,l+n2+1):
            #if the low of the candle is higher than the low of the next candle
            if(df1.Low[i]<df1.Low[i-1]):
                return 0
        return 1
    
    def resistance(df1, l, n1, n2)->1 or 0: 
        #df1 is the dataframe
        #l is the row
        #n1 is the number of candles before
        #n2 is the number of candles after
        for i in range(l-n1+1, l+1):
            #if the high of the candle is lower than the high of the previous candle
            if(df1.High[i]<df1.High[i-1]):
                return 0
        for i in range(l+1,l+n2+1):
            #if the high of the candle is lower than the high of the next candle
            if(df1.High[i]>df1.High[i-1]):
                return 0
        return 1
        
    #sr = support and resistance
    sr = []
    #n1 is the number of candles before
    n1=3
    #n2 is the number of candles after
    n2=2
    
    #check for support and resistance
    for row in range(3, len(df)-n2): #len(df)-n2
        if support(df, row, n1, n2):
            #append the row, the low of the candle and 1 for support
            sr.append((row,df.Low[row],1))
        if resistance(df, row, n1, n2):
            #append the row, the high of the candle and 2 for resistance
            sr.append((row,df.High[row],2))
  
    
    #s is the start of the graph
    s = 0
    #e is the end of the graph
    e = len(df)-2
    #dfpl is the dataframe for the graph
    dfpl = df[s:e]
    
    #plot the candlestick graph
    fig = go.Figure(data=[go.Candlestick(x=dats, open=dfpl['Open'], high=dfpl['High'], low=dfpl['Low'], close=dfpl['Close/Last'])])
    
    
    #add zoomer on the y axis
    fig.update_layout(
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )       

    c=0

    #add support and resistance lines to the graph
    for i in sr:
        if i[2]==1:
            #add a green line for support
            fig.add_shape(type="line",
                x0=i[0], y0=i[1], x1=i[0]+20*(n1+n2), y1=i[1], line=dict(color="green",width=1))
        else:
            fig.add_shape(type="line",
                #add a red line for resistance
                x0=i[0], y0=i[1], x1=i[0]+20*(n1+n2), y1=i[1], line=dict(color="red",width=1))
        c+=1
    
    fig.show()