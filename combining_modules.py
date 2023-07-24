from support_resistance import detection_support_resistance
from trendline_detection import trendline_detect
from moving_average import moving_average
import pandas as pd
import plotly.graph_objects as go
def main(file:str,num_back_candles: int = 70, back_candle_range: int = 50, window_size: int = 7,record_to_plot: int = 2000,):

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

    # Reset the index of the dataset
    financial_data.reset_index(drop=True, inplace=True)
    financial_data

    # Print the first 10 rows of the dataset
    print(financial_data.head(10))

    data_to_plot = financial_data[:record_to_plot]

    #initialise the figure
    fig = go.Figure(data=[go.Candlestick(x=data_to_plot.index,
                                        open=data_to_plot['Close/Last'],
                                        high=data_to_plot['High'],
                                        low=data_to_plot['Low'],
                                        close=data_to_plot['Open'])])
    
    fig.update_layout(
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )
    





    
    trendline_detect(financial_data, num_back_candles=20, back_candle_range=10, window_size=3,record_to_plot=record_to_plot,fig=fig)
    #detection_support_resistance(financial_data,record_to_plot,fig)
    #moving_average(financial_data,record_to_plot,fig)
    fig.show()


main(file="data_nasdaq\HistoricalData_SBUX.csv")