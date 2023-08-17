from backtesting import Backtest, Strategy
from moving_average import moving_average




def moving_average_backtest(financial_data,record_to_plot,fig=None):
    #financial_data = financial_data[::-1]
    financial_data = moving_average(financial_data,record_to_plot,fig,dates=[7,15,40])


    def SIGNAL():
            return financial_data.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            self.signal = self.I(SIGNAL)

        def next(self):
            if self.signal > 0:
                self.buy()
            elif self.signal < 0:
                self.sell()

    bt = Backtest(financial_data, MyCandlesStrat, cash=10_000, commission=.00)
    stat = bt.run()
    print(stat)

        #how many trades were made
    
    bt.plot()
