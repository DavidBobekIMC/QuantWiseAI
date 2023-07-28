from backtesting import Backtest, Strategy
from moving_average import moving_average




def moving_average_backtest(financial_data,record_to_plot,fig=None):
    #financial_data = financial_data[::-1]
    financial_data = moving_average(financial_data,record_to_plot,fig)


    def SIGNAL():
            return financial_data.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next()
            if self.signal1 == 1:
                sl1 = self.data.Close[-1] - 600e-4
                tp1 = self.data.Close[-1] + 450e-4
                self.buy(sl=sl1, tp=tp1)
            elif self.signal1 == -1:
                sl1 = self.data.Close[-1] + 600e-4
                tp1 = self.data.Close[-1] - 450e-4
                self.sell(sl=sl1, tp=tp1)

    bt = Backtest(financial_data, MyCandlesStrat, cash=10_000, commission=.00)
    stat = bt.run()
    print(stat)

        #how many trades were made
    
    bt.plot()
