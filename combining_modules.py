from support_resistance import detection_support_resistance
from trendline_detection import trendline_detect
from moving_average import moving_average
from backtesting_module import backtesting
from moving_average_backtest import moving_average_backtest
import pandas as pd

import plotly.graph_objects as go
def main(file:str,num_back_candles: int = 70, back_candle_range: int = 50, window_size: int = 7,record_to_plot:int=2000,fig:go.Figure=None):

    financial_data = pd.read_csv(file)

    #delete dollar sign
    try:
        # Clean up dollar signs and convert columns to numeric values
        financial_data["Close/Last"] = financial_data["Close/Last"].str.replace("$", "").astype(float)
        financial_data["Open"] = financial_data["Open"].str.replace("$", "").astype(float)
        financial_data["High"] = financial_data["High"].str.replace("$", "").astype(float)
        financial_data["Low"] = financial_data["Low"].str.replace("$", "").astype(float)
    except:
        pass
    
    #rename the headers
    try:
        
        financial_data.rename(columns={"Close/Last":"Close"}, inplace=True)
    except:
        pass    
    
    
    financial_data.rename(columns={"high":"High"}, inplace=True)
    financial_data.rename(columns={"low":"Low"}, inplace=True)
    financial_data.rename(columns={"open":"Open"}, inplace=True)
    financial_data.rename(columns={"volume":"Volume"}, inplace=True)
    financial_data.rename(columns={"close":"Close"}, inplace=True)
    financial_data.reset_index(drop=True, inplace=True)

    

    # Reset the index of the dataset
    financial_data = financial_data.reset_index(drop=True)
        
    # Print the first 10 rows of the dataset
    print(financial_data.head(10))

    data_to_plot = financial_data[:len(financial_data)]
    
    #initialise the figure
    fig = go.Figure(data=[go.Candlestick(x=data_to_plot.index,
                                        open=data_to_plot['Open'],
                                        high=data_to_plot['High'],
                                        low=data_to_plot['Low'],
                                        close=data_to_plot['Close'])])
    
    
    #revert xaxis
    #fig.update_xaxes(autorange="reversed")
    
    fig.update_layout(
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )
    





    
    #trendline_detect(financial_data, num_back_candles=20, back_candle_range=10, window_size=3,record_to_plot=record_to_plot,fig=fig)
    #detection_support_resistance(financial_data,record_to_plot,fig)
    
    #Moving average is adding extra columns to the dataframe so need to fix this
    #moving_average(financial_data,record_to_plot=len(financial_data),fig=fig)
    #backtesting(financial_data,record_to_plot,fig)
    moving_average_backtest(financial_data,record_to_plot=20000,fig=fig)
    fig.show()


#main(file="data_nasdaq\HistoricalData_SBUX.csv")
main(file="data\EURGBP_Candlestick_4_Hour_BID_23.07.2013-22.07.2023.csv")