import pandas_ta as pa
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


def moving_average(financial_data:pd.DataFrame,record_to_plot:int=2000,fig:go.Figure=None):
    #rename column from Close/Last to Close
    financial_data.rename(columns={"Close/Last":"Close"}, inplace=True)
    financial_data["MA20"] = pa.ema(financial_data.Close, length=20)
    financial_data["MA30"] = pa.ema(financial_data.Close, length=30)
    financial_data["MA60"] = pa.ema(financial_data.Close, length=60)
    financial_data.tail(10)

    def mysig(x):
        if x.MA20<x.MA30<x.MA60:
            return -1
        elif x.MA20>x.MA30>x.MA60:
            return +1
        else:
            return 0
    
    financial_data["signal"] = financial_data.apply(mysig, axis=1)

    dfpl = financial_data[:record_to_plot]
    
    
 
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA20, mode='lines', name='MA20'))
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA30, mode='lines', name='MA30'))
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MA60, mode='lines', name='MA60'))

   


    # how many signals were there
    print("There were", len(dfpl[dfpl.signal != 0]), "signals")