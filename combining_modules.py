from support_resistance import detection_support_resistance
from trendline_detection import trendline_detect
from moving_average import moving_average
from backtesting_module import backtesting
from moving_average_backtest import moving_average_backtest
from arima_module import arima_model
from choch_module import choch
import pandas as pd
from engulfing_pattern_star_pattern import detectCustomPatterns
#from rolling_window import rolling_window
from backtesting import Strategy, Backtest
from rsi import calculate_qqe_rsi_trailing_stop
from vold_ratio_module import void_ratio
from macd_module import calculate_macd
from PPSRMA import ppsrma
import plotly.graph_objects as go
import backtrader as bt

def main(file: str, num_back_candles: int = 70, back_candle_range: int = 50, window_size: int = 7, record_to_plot: int = 2000, fig: go.Figure = None):
    # sourcery skip: use-contextlib-suppress

    financial_data = pd.read_csv(file)

    # delete dollar sign
    try:
        # Clean up dollar signs and convert columns to numeric values
        financial_data["Close/Last"] = financial_data["Close/Last"].str.replace(
            "$", "").astype(float)
        financial_data["Open"] = financial_data["Open"].str.replace(
            "$", "").astype(float)
        financial_data["High"] = financial_data["High"].str.replace(
            "$", "").astype(float)
        financial_data["Low"] = financial_data["Low"].str.replace(
            "$", "").astype(float)
    except Exception:
        pass

    # rename the headers
    try:
        financial_data.rename(columns={"Close/Last": "Close"}, inplace=True)
    except Exception:
        pass



    #if financial_data.iloc[0]['Close'] > financial_data.iloc[-1]['Close']:
    #    financial_data = financial_data[::-1]

    financial_data.rename(columns={"high": "High"}, inplace=True)
    financial_data.rename(columns={"low": "Low"}, inplace=True)
    financial_data.rename(columns={"open": "Open"}, inplace=True)
    financial_data.rename(columns={"volume": "Volume"}, inplace=True)
    financial_data.rename(columns={"close": "Close"}, inplace=True)

    # Reset the index of the dataset
    financial_data = financial_data.reset_index(drop=True)
    #financial_data = financial_data[:2000]
    # Print the first 10 rows of the dataset
    print(financial_data.head(10))

    data_to_plot = financial_data[:]

    # initialise the figure
    fig = go.Figure(data=[go.Candlestick(x=data_to_plot.index,
                                         open=data_to_plot['Open'],
                                         high=data_to_plot['High'],
                                         low=data_to_plot['Low'],
                                         close=data_to_plot['Close'])])

    # revert xaxis
    # fig.update_xaxes(autorange="reversed")

    fig.update_layout(
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )



    #financial_data = trendline_detect(financial_data, num_back_candles=20, back_candle_range=10, window_size=3,record_to_plot=record_to_plot,fig=fig)
    # detection_support_resistance(financial_data,record_to_plot,fig)

    # Moving average is adding extra columns to the dataframe so need to fix this
    financial_data = moving_average(financial_data,record_to_plot=len(financial_data),fig=fig,dates=[7,15,21,60,120])
    #backtesting(financial_data,record_to_plot=10000,fig=fig)
    # moving_average_backtest(financial_data,record_to_plot=2000,fig=fig)
    #financial_data = arima_model(financial_data, record_to_plot=500, fig=fig)
    #financial_data = choch(financial_data, record_to_plot=2000, fig=fig)
    #financial_data = detectCustomPatterns(financial_data=financial_data,fig=fig)
    #financial_data = rolling_window(financial_data=financial_data, record_to_plot=2000)
    #financial_data = calculate_qqe_rsi_trailing_stop(financial_data=financial_data, record_to_plot=1200)
    #financial_data = calculate_macd(financial_data=financial_data, record_to_plot=2000)
    #financial_data = ppsrma(financial_data=financial_data, record_to_plot=1999)
    #financial_data = doncian_channels_ML(financial_data=financial_data)

    #financial_data = void_ratio(financial_data=financial_data, record_to_plot=1500)
    def SIGNAL():
        return financial_data.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)
        def next(self):
            super().next()
            if self.signal1 == 2:
                # Buy
                sl1 = self.data.Close[-1] - 600e-4
                tp1 = self.data.Close[-1] + 450e-4

                self.buy(sl=sl1, tp=tp1)

            elif self.signal1 == 1:
                sl1 = self.data.Close[-1] + 600e-4
                tp1 = self.data.Close[-1] - 450e-4
                self.sell(sl=sl1, tp=tp1)



    # Run the backtest

    def apply_backtest(financial_data: pd.DataFrame ):
        bt = Backtest(financial_data, MyCandlesStrat, cash=10_000, commission=.00)
        stat = bt.run()


        bt.plot()
        print(stat)

        count_buy = 0
        count_sell = 0
        for i in financial_data.signal:
            if i == 2:
                count_buy += 1
            elif i == 1:
                count_sell += 1

        print(count_buy)
        print(count_sell)

    

    if financial_data.get('signal') is not None:
        apply_backtest(financial_data=financial_data)
       

        
#main(file="data_nasdaq\HistoricalData_SBUX.csv")
#main(file="data_nasdaq\HistoricalData_MSFT.csv")
main(file="data\EURUSD_Candlestick_4_Hour_ASK_05.05.2003-16.10.2021.csv")