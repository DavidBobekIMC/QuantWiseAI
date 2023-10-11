import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
# Important library for backtesting
from backtesting import Strategy, Backtest
from support_resistance import support, resistance


def backtesting(df: pd.DataFrame, record_to_plot: int = 2000, fig: go.Figure = None):
    df = df[:record_to_plot]
    df.reset_index(drop=True, inplace=True)
    df.isna().sum()
    df.tail()

    def support(df1, l, n1, n2):  # n1 n2 before and after candle l
        for i in range(l-n1+1, l+1):
            if (df1.Low[i] > df1.Low[i-1]):
                return 0
        for i in range(l+1, l+n2+1):
            if (df1.Low[i] < df1.Low[i-1]):
                return 0
        return 1

    def resistance(df1, l, n1, n2):  # n1 n2 before and after candle l
        for i in range(l-n1+1, l+1):
            if (df1.High[i] < df1.High[i-1]):
                return 0
        for i in range(l+1, l+n2+1):
            if (df1.High[i] > df1.High[i-1]):
                return 0
        return 1

    length = len(df)
    high = list(df['High'])
    low = list(df['Low'])
    close = list(df['Close'])
    open = list(df['Open'])
    bodydiff = [0] * length

    highdiff = [0] * length
    lowdiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length

    def isEngulfing(l):
        row = l
        bodydiff[row] = abs(open[row]-close[row])
        if bodydiff[row] < 0.000001:
            bodydiff[row] = 0.000001

        bodydiffmin = 0.002
        if (bodydiff[row] > bodydiffmin and bodydiff[row-1] > bodydiffmin and
            open[row-1] < close[row-1] and
            open[row] > close[row] and
                (open[row]-close[row-1]) >= -0e-5 and close[row] < open[row-1]):  # +0e-5 -5e-5
            return 1

        elif (bodydiff[row] > bodydiffmin and bodydiff[row-1] > bodydiffmin and
              open[row-1] > close[row-1] and
              open[row] < close[row] and
              (open[row]-close[row-1]) <= +0e-5 and close[row] > open[row-1]):  # -0e-5 +5e-5
            return 2
        else:
            return 0

    def isStar(l):
        bodydiffmin = 0.0020
        row = l
        highdiff[row] = high[row]-max(open[row], close[row])
        lowdiff[row] = min(open[row], close[row])-low[row]
        bodydiff[row] = abs(open[row]-close[row])
        if bodydiff[row] < 0.000001:
            bodydiff[row] = 0.000001
        ratio1[row] = highdiff[row]/bodydiff[row]
        ratio2[row] = lowdiff[row]/bodydiff[row]

        # and open[row]>close[row]):
        if (ratio1[row] > 1 and lowdiff[row] < 0.2*highdiff[row] and bodydiff[row] > bodydiffmin):
            return 1
        # and open[row]<close[row]):
        elif (ratio2[row] > 1 and highdiff[row] < 0.2*lowdiff[row] and bodydiff[row] > bodydiffmin):
            return 2
        else:
            return 0

    def closeResistance(l, levels, lim):
        if len(levels) == 0:
            return 0
        c1 = abs(
            df.High[l]-min(levels, key=lambda x: abs(x-df.High[l]))) <= lim
        c2 = abs(max(df.Open[l], df.Close[l])-min(levels,
                 key=lambda x: abs(x-df.High[l]))) <= lim
        c3 = min(df.Open[l], df.Close[l]) < min(
            levels, key=lambda x: abs(x-df.High[l]))
        c4 = df.Low[l] < min(levels, key=lambda x: abs(x-df.High[l]))
        if ((c1 or c2) and c3 and c4):
            return 1
        else:
            return 0

    def closeSupport(l, levels, lim):
        if len(levels) == 0:
            return 0
        c1 = abs(df.Low[l]-min(levels, key=lambda x: abs(x-df.Low[l]))) <= lim
        c2 = abs(min(df.Open[l], df.Close[l])-min(levels,
                 key=lambda x: abs(x-df.Low[l]))) <= lim
        c3 = max(df.Open[l], df.Close[l]) > min(
            levels, key=lambda x: abs(x-df.Low[l]))
        c4 = df.High[l] > min(levels, key=lambda x: abs(x-df.Low[l]))
        if ((c1 or c2) and c3 and c4):
            return 1
        else:
            return 0

    n1 = 2
    n2 = 2
    backCandles = 40
    signal = [0] * length

    for row in range(backCandles, len(df)-n2):
        ss = []
        rr = []
        for subrow in range(row-backCandles+n1, row+1):
            if support(df, subrow, n1, n2):
                ss.append(df.Low[subrow])
            if resistance(df, subrow, n1, n2):
                rr.append(df.High[subrow])
        #!!!! parameters
        # and df.RSI[row]<30
        if ((isEngulfing(row) == 1 or isStar(row) == 1) and closeResistance(row, rr, 150e-5)):
            signal[row] = 1
        # and df.RSI[row]>70
        elif ((isEngulfing(row) == 2 or isStar(row) == 2) and closeSupport(row, ss, 150e-5)):
            signal[row] = 2
        else:
            signal[row] = 0

    df['signal'] = signal
    df[df['signal'] == 1].count()

    report = {"up": 0, "down": 0, "total": 0}
    report['up'] = df[df['signal'] == 1].count()[0]
    report['down'] = df[df['signal'] == 2].count()[0]
    report['total'] = df[df['signal'] != 0].count()[0]

    # plot distribution of signals
    plt.figure(figsize=(10, 5))
    plt.title("Distribution of signals")
    plt.xlabel("Signal")
    plt.ylabel("Count")
    plt.hist(df['signal'], bins=3, color='blue',
             edgecolor='black', linewidth=1.2)
    plt.show()

    df.columns = ['Local time', 'Open', 'High',
                  'Low', 'Close', 'Volume', 'signal']
    
    
    
    

    def SIGNAL():
        return df.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next()
            if self.signal1 == 2:
                sl1 = self.data.Close[-1] - 600e-4
                tp1 = self.data.Close[-1] + 450e-4
                self.buy(sl=sl1, tp=tp1)
            elif self.signal1 == 1:
                sl1 = self.data.Close[-1] + 600e-4
                tp1 = self.data.Close[-1] - 450e-4
                self.sell(sl=sl1, tp=tp1)

    bt = Backtest(df, MyCandlesStrat, cash=10_000, commission=.00)
    stat = bt.run()
    print(stat)
    bt.plot()
