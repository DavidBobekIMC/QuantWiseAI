import pandas_ta as pa
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

def moving_average(financial_data:pd.DataFrame,record_to_plot:int=2000,fig:go.Figure=None):
    #rename column from Close/Last to Close
    financial_data = financial_data[::-1]
    financial_data.rename(columns={"Close/Last":"Close"}, inplace=True)
    
    financial_data["MA20"] = pa.ema(financial_data.Close, length=20)
    financial_data["MA50"] = pa.ema(financial_data.Close, length=50)
    
    
    
    #financial_data["MA7"] = pa.sma(financial_data.Close, length=7)
    #financial_data["MA15"] = pa.sma(financial_data.Close, length=15)
    #financial_data["MA21"] = pa.sma(financial_data.Close, length=21)
    
    #financial_data["MA60"] = pa.ema(financial_data.Close, length=60)
    #financial_data["MA120"] = pa.ema(financial_data.Close, length=120)
    financial_data.tail(10)

    
    
    
    def mysig(x):
        if x["MA20"] > x["MA50"]:
            return 1
        elif x["MA20"] < x["MA50"]:
            return -1
     
    
    financial_data["signal"] = financial_data.apply(mysig, axis=1)
    dfpl = financial_data[:record_to_plot]
    
    
 
    #fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA20, mode='lines', name='MA20'))
    #fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA30, mode='lines', name='MA30'))
    #fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA60, mode='lines', name='MA60'))
    #fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA120, mode='lines', name='MA120'))

   


    # how many signals were there
    print("There were", len(financial_data[financial_data["signal"] == 1]), "buy signals")
    print("There were", len(financial_data[financial_data["signal"] == -1]), "sell signals")
    
    #day one 
    print("day one",financial_data.iloc[0])
    #day last
    print("day last",financial_data.iloc[-1])
    return dfpl