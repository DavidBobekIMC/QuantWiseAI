import pandas as pd
import matplotlib.pyplot as plt


def ppsrma(financial_data: pd.DataFrame, record_to_plot: int=2000):
    financial_data = financial_data[:record_to_plot]
    # Define the input parameters as constants
    pctP = 66
    pblb = 6
    pctS = 5

    # Display the PinBars, Shaved Bars, Inside Bars, Outside Bars
    spb = False
    ssb = False
    sib = False
    sob = False
    sgb = False

    # Display the Daily, Weekly, Monthly, Quarterly, Yearly Projected Highs and Lows
    sd = False

    # Display the SMA and EMA
    SMA_EMA = True
    len = 25
    src = financial_data['Close']
    SMA_EMA1 = True
    len1 = 50
    src1 = financial_data['Close']

    # Calculate necessary variables
    pctCp = pctP * 0.01
    pctCPO = 1 - pctCp
    pctCs = pctS * 0.01
    pctSPO = pctCs
    high = financial_data['High']
    low = financial_data['Low']
    range = high - low

    # PinBars
    def pBarUp():
        return spb and (financial_data['Open'] > high - (range * pctCPO)) and (financial_data['Close'] > high - (range * pctCPO)) and (financial_data['Low'] <= financial_data['Low'].rolling(pblb).min())

    def pBarDn():
        return spb and (financial_data['Open'] < high - (range * pctCp)) and (financial_data['Close'] < high - (range * pctCp)) and (high >= high.rolling(pblb).max())

    # Shaved Bars
    def sBarUp():
        return ssb and (financial_data['Close'] >= (high - (range * pctCs)))

    def sBarDown():
        return ssb and (financial_data['Close'] <= (low + (range * pctCs)))

    # Inside Bars
    def insideBar():
        return sib and (high <= high.shift(1)) and (low >= low.shift(1))

    # Outside Bars
    def outsideBar():
        return sob and (high > high.shift(1)) and (low < low.shift(1))

    # PinBars
    financial_data['pBarUp'] = pBarUp()
    financial_data['pBarDn'] = pBarDn()

    # Shaved Bars
    financial_data['sBarUp'] = sBarUp()
    financial_data['sBarDown'] = sBarDown()

    # Inside and Outside Bars
    financial_data['insideBar'] = insideBar()
    financial_data['outsideBar'] = outsideBar()

    financial_data['hlc3'] = (
        financial_data['High'] + financial_data['Low'] + financial_data['Close']) / 3

    # Color Bars
    bar_colors = []

    for i in financial_data.index:
        if financial_data['pBarUp'][i]:
            bar_colors.append('lime')
        elif financial_data['pBarDn'][i]:
            bar_colors.append('red')
        elif financial_data['sBarDown'][i]:
            bar_colors.append('fuchsia')
        elif financial_data['sBarUp'][i]:
            bar_colors.append('aqua')
        elif financial_data['insideBar'][i]:
            bar_colors.append('yellow')
        elif financial_data['outsideBar'][i]:
            bar_colors.append('orange')
        else:
            bar_colors.append('gray' if sgb else 'na')

    financial_data['bar_colors'] = bar_colors

    print(financial_data.head(10))
    # Plot the data
    plt.figure(figsize=(14, 7))
    plt.plot(financial_data.index,
             financial_data['Close'], label='Close Price', color='blue')

    if SMA_EMA:
        fast_sma = src.rolling(len).mean()
        fast_ema = src.ewm(span=len, adjust=False).mean()
        plt.plot(financial_data.index, fast_sma,
                 label='MA Fast', color='yellow', linewidth=1)
        plt.plot(financial_data.index, fast_ema,
                 label='EMA Fast', color='orange', linewidth=1)

    if SMA_EMA1:
        med_sma1 = src1.rolling(len1).mean()
        med_ema1 = src1.ewm(span=len1, adjust=False).mean()
        plt.plot(financial_data.index, med_sma1,
                 label='MA Medium', color='fuchsia', linewidth=2)
        plt.plot(financial_data.index, med_ema1,
                 label='EMA Medium', color='black', linewidth=2)

    # Display the Daily, Weekly, Monthly, Quarterly, Yearly Projected Highs and Lows

    if sd:
        # Daily Projected High Low
        dtime_pf = financial_data['hlc3'].shift(1) * 2
        # dtime_pl: Daily Projected Low
        # dtime_ph: Daily Projected High
        dtime_pl = dtime_pf - financial_data['High'].shift(1)
        dtime_ph = dtime_pf - financial_data['Low'].shift(1)

        # RED = close price is less than the corresponding calculated value of 'dtime_pl.
        # BROWN = close price is greater than the corresponding calculated value of 'dtime_pl.

        # LIME = close price is greater than the corresponding calculated value of 'dtime_ph.
        # PURPLE = close price is less than the corresponding calculated value of 'dtime_ph.
        pcolor_pl = ['red' if c < d else 'brown' for c,
                     d in zip(financial_data['Close'], dtime_pl)]
        pcolor_ph = ['lime' if c > d else 'purple' for c,
                     d in zip(financial_data['Close'], dtime_ph)]
        # plt.scatter(financial_data.index, dtime_pl, c=pcolor_pl, label='Daily Projected Low', s=100, marker='.', linewidth=2,)
        # plt.scatter(financial_data.index, dtime_ph, c=pcolor_ph, label='Daily Projected High', s=100, marker='.', linewidth=2)

        # plot lines
        plt.plot(financial_data.index, dtime_pl,
                 label='Daily Projected Low', color='brown', linewidth=1)
        plt.plot(financial_data.index, dtime_ph,
                 label='Daily Projected High', color='purple', linewidth=1)

        # fill the region between the lines
        plt.fill_between(financial_data.index, dtime_pl,
                         dtime_ph, alpha=0.1, color='purple')
        plt.fill_between(financial_data.index, dtime_ph,
                         dtime_pl, alpha=0.1, color='brown')

    last_call = 0
    financial_data['signal'] = 0
    count = 0
    for i in financial_data.index:
        count += 1
        # if meds>fasts = sell
        # if meds<fasts = buy
        if (med_ema1[i] and med_ema1[i]) > (fast_ema[i] and fast_sma[i]):
            if last_call != 1:
                plt.scatter(
                    i, financial_data['Low'][i], c='red', label='Sell', s=100, marker='v', linewidth=1)
                last_call = 1
                financial_data['signal'][i] = 1
                continue
        
                
        if (med_ema1[i] and med_ema1[i]) < (fast_ema[i] and fast_sma[i]):
            if last_call != 2:
                plt.scatter(
                    i, financial_data['Low'][i], c='lime', label='Buy', s=100, marker='^', linewidth=1)
                last_call = 2
                financial_data['signal'][i] = 2
                continue
          
        financial_data['signal'][i] = 0
                
     
    
    # Plot the PinBars
    # plt.scatter(financial_data.index, financial_data['Low'], c=financial_data['bar_colors'], label='PinBars', s=100, marker='o', linewidth=1)

    # Plot the Shaved Bars
    # plt.scatter(financial_data.index, financial_data['Low'], c=financial_data['bar_colors'], label='Shaved Bars', s=100, marker='o', linewidth=1)

    # Plot the Inside and Outside Bars
    # plt.scatter(financial_data.index, financial_data['Low'], c=financial_data['bar_colors'], label='Inside/Outside Bars', s=100, marker='o', linewidth=1)

    # Plot the Candlestick Bars
    # plt.scatter(financial_data.index, financial_data['Low'], c=financial_data['bar_colors'], label='Candlestick Bars', s=100, marker='o', linewidth=1)

    plt.legend(loc='upper left')
    plt.show()
    return financial_data
