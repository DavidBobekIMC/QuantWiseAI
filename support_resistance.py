import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

def detection_support_resistance(financial_data:pd.DataFrame,record_to_plot:int=2000,fig:go.Figure=None)->pd.DataFrame:
    #sr = support and resistance
    sr = []
    #n1 is the number of candles before
    n1=3
    #n2 is the number of candles after
    n2=2
    
    #check for support and resistance
    for row in range(3, record_to_plot-n2): #len(financial_data)-n2
        if support(financial_data, row, n1, n2):
            #append the row, the low of the candle and 1 for support
            sr.append((row,financial_data.Low[row],1))
        if resistance(financial_data, row, n1, n2):
            #append the row, the high of the candle and 2 for resistance
            sr.append((row,financial_data.High[row],2))
            
            
    #add zoomer on the y axis
           

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
    

  
    
def support(financial_data1, l, n1, n2)->1 or 0:
    #financial_data1 is the dataframe
    #l is the row
    #n1 is the number of candles before
    #n2 is the number of candles after
    
    for i in range(l-n1+1, l+1):
        #if the low of the candle is higher than the low of the previous candle
        if(financial_data1.Low[i]>financial_data1.Low[i-1]):
            return 0
        
    
    for i in range(l+1,l+n2+1):
        #if the low of the candle is higher than the low of the next candle
        if(financial_data1.Low[i]<financial_data1.Low[i-1]):
            return 0
    return 1

def resistance(financial_data1, l, n1, n2)->1 or 0: 
    #financial_data1 is the dataframe
    #l is the row
    #n1 is the number of candles before
    #n2 is the number of candles after
    for i in range(l-n1+1, l+1):
        #if the high of the candle is lower than the high of the previous candle
        if(financial_data1.High[i]<financial_data1.High[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        #if the high of the candle is lower than the high of the next candle
        if(financial_data1.High[i]>financial_data1.High[i-1]):
            return 0
    return 1
        
    
    

    
    
    