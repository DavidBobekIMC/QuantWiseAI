
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


from pmdarima import auto_arima


def choch(financial_data: pd.DataFrame, record_to_plot: int = 2000, fig: go.Figure = None, dates=None) -> go.Figure:
    financial_data = financial_data[:record_to_plot]
    financial_data["RSI"] = ta.rsi(financial_data.loc[:, "Close"])
    financial_data["EMA"] = ta.ema(financial_data.loc[:, "Close"])

    EMAsignal = [0] * len(financial_data)
    back_candle_range = 20

    for i in range(back_candle_range, len(financial_data)):
        up_trend = 1
        down_trend = 1
        for j in range(i-back_candle_range, i+1):
            if financial_data["Close"][j] > financial_data["EMA"][j]:
                down_trend = 0
            elif financial_data["Close"][j] < financial_data["EMA"][j]:
                up_trend = 0
        if up_trend == 1 and down_trend == 1:
            EMAsignal[i] = 3
        elif up_trend == 1:
            EMAsignal[i] = 2

        elif down_trend == 1:
            EMAsignal[i] = 1
    financial_data["EMASignal"] = EMAsignal

    def is_pivot_point(candle, window):
        """
        function that detects if a candle is a pivot/fractal point
        args: candle index, window before and after candle to test if pivot
        returns: 1 if pivot high, 2 if pivot low, 3 if both and 0 default
        """
        if candle-window < 0 or candle+window >= len(financial_data):
            return 0

        pivotHigh = 1
        pivotLow = 2
        for i in range(candle-window, candle+window+1):
            if financial_data.iloc[candle]["Close"] > financial_data.iloc[i]["Close"]:
                pivotLow = 0
            if financial_data.iloc[candle]["Open"] < financial_data.iloc[i]["Open"]:
                pivotHigh = 0
        if (pivotHigh and pivotLow):
            return 3
        elif pivotHigh:
            return pivotHigh
        elif pivotLow:
            return pivotLow
        else:
            return 0

    window = 10

    financial_data["isPivotPoint"] = financial_data.apply(
        lambda x: is_pivot_point(x.name, window), axis=1)

    def pointpos(x):
        if x["isPivotPoint"] == 1:
            return x["Close"]*1.01
        elif x["isPivotPoint"] == 2:
            return x["Close"]*0.99
        else:
            return None

    financial_data["pointpos"] = financial_data.apply(
        lambda x: pointpos(x), axis=1)

    fig.add_trace(go.Scatter(x=financial_data.index,
                             y=financial_data['pointpos'], name=f'Pivot Point',    marker=dict(size=6, color="turquoise"), mode="markers"))

    def detect_structure(candle, backcandles, window):
        """
        Attention! window should always be greater than the pivot window! to avoid look ahead bias
        """
        localdf = financial_data[candle-backcandles-window:candle-window]
        highs = localdf[localdf["isPivotPoint"] == 1]["High"].values
        lows = localdf[localdf["isPivotPoint"] == 2]["Low"].values
        highsidx = localdf[localdf["isPivotPoint"] == 1].index
        lowsidx = localdf[localdf["isPivotPoint"] == 2].index

        pattern_detected = True

        lim1 = 0.005
        lim2 = lim1/3

        if len(highs) == 3 and len(lows) == 3:
            order_condition = (lowsidx[0] < highsidx[0]
                               < lowsidx[1] < highsidx[1]
                               < lowsidx[2] < highsidx[2])
            diff_condition = (
                abs(lows[0]-highs[0]) > lim1 and
                abs(highs[0]-lows[1]) > lim2 and
                abs(highs[1]-lows[1]) > lim1 and
                abs(highs[1]-lows[2]) > lim2
            )
            pattern_1 = (lows[0] < highs[0] and
                         lows[1] > lows[0] and lows[1] < highs[0] and
                         highs[1] > highs[0] and
                         lows[2] > lows[1] and lows[2] < highs[1] and
                         highs[2] < highs[1] and highs[2] > lows[2]
                         )

            pattern_2 = (lows[0] < highs[0] and
                         lows[1] > lows[0] and lows[1] < highs[0] and
                         highs[1] > highs[0] and
                         lows[2] < lows[1] and
                         highs[2] < highs[1]
                         )

            if (order_condition and
                diff_condition and
                (pattern_1 or pattern_2)
                ):
                pattern_detected = True

        if pattern_detected:
            return 1
        else:
            return 0

    financial_data['pattern_detected'] = financial_data.index.map(
        lambda x: detect_structure(x, backcandles=40, window=6))

    print(financial_data[financial_data['pattern_detected'] == 1])

    fig.add_trace(go.Scatter(x=financial_data[financial_data['pattern_detected'] == 1].index,
                             y=financial_data[financial_data['pattern_detected'] == 1]['Close'], name=f'Pattern',    marker=dict(size=4, color="purple"), mode="markers"))

    fig.show()