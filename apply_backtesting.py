import pandas as pd
from backtesting import Strategy, Backtest


def backtester(financial_data):
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
        stats = bt.run()

        count_buy = 0
        count_sell = 0
        for i in financial_data.signal:
            if i == 2:
                count_buy += 1
            elif i == 1:
                count_sell += 1

        print(count_buy)
        print(count_sell)
        return bt,stats
        
    if financial_data.get('signal') is not None:
        bt , stats = apply_backtest(financial_data)
        return (bt,stats)