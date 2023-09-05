import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def void_ratio(financial_data: pd.DataFrame, record_to_plot: int = None):
    # Calculate vold ratio
    # Can only use .dt accessor with datetimelike values
    # time data "13.05.2003 01:00:00.000" doesn't match format "%m.%d.%Y %H:%M:%S.%f",
    # try "13.05.2003 01:00:00.000" instead
    financial_data['date'] = pd.to_datetime(
        financial_data['date'], format="%d.%m.%Y %H:%M:%S.%f")
    financial_data = financial_data[:record_to_plot]
    is_new_time = np.append(
        np.diff(financial_data['date']) > pd.Timedelta(seconds=0), True)

    up_net_volume = np.where(
        financial_data['Close'] > financial_data['Open'], financial_data['Volume'], 0)
    down_net_volume = np.where(
        financial_data['Close'] < financial_data['Open'], financial_data['Volume'], 0)

    up_vol = np.nan
    down_vol = np.nan
    unv = []
    dnv = []

    for idx, new_time in enumerate(is_new_time):
        if new_time:
            up_vol = up_net_volume[idx]
            down_vol = down_net_volume[idx]
            unv.append(up_vol)
            dnv.append(down_vol)
        else:
            if not np.isnan(up_vol):
                up_vol = up_net_volume[idx]
                unv.append(up_vol)
            if not np.isnan(down_vol):
                down_vol = down_net_volume[idx]
                dnv.append(down_vol)

    net_valup = np.sum(unv)
    net_valdown = np.sum(dnv)

    vold = net_valup / net_valdown

    # Plot vold ratio
    plt.figure(figsize=(10, 6))
    plt.plot(financial_data.index, [
             vold] * len(financial_data.index), label='VOLD Ratio', color='white', alpha=0.5)

    # Bollinger Bands
    length = 50
    src = vold
    mult = 2.0

    basis = financial_data['Close'].rolling(window=length).mean()
    dev = mult * financial_data['Close'].rolling(window=length).std()
    upper = basis + dev
    lower = basis - dev

    # Signalling
    # Buy when the Close price crosses above the
    # Sell when the Close price crosses below the lower band

    financial_data["signal"] = 0

    # if the close price is greater than the basis, and lower than the upper band, buy
    # if the close price is greater than the upper band
    # if the close price is less than the lower band sell
    # if the close price is less than the basis, and greater than the lower band, sell
    last_signal = None
    for i in range(length, len(financial_data)):
        if financial_data['Close'][i] > basis[i] and i < len(financial_data):          
                    if last_signal != 'buy':
                        plt.plot(i, financial_data['Close'][i], marker='o', color='red')
                        last_signal = 'buy'
                        financial_data["signal"][i] = 2
                        continue
                        
                    
        if financial_data['Close'][i] > upper[i] and i < len(financial_data):
            if last_signal != 'sell':
                plt.plot(i, financial_data['Close'][i], marker='o', color='green')
                last_signal = 'sell'
                financial_data["signal"][i] = 1
                continue
        if financial_data['Close'][i] < lower[i] and i < len(financial_data):
            if last_signal != 'buy' :
                plt.plot(i, financial_data['Close'][i], marker='o', color='red')
                last_signal = 'buy'
                financial_data["signal"][i] = 2
                continue
        if financial_data['Close'][i] < basis[i] and i < len(financial_data):
            if last_signal != 'sell':
                plt.plot(i, financial_data['Close'][i], marker='o', color='green')
                last_signal = 'sell'
                financial_data["signal"][i] = 1
                continue
                

    plt.plot(financial_data.index, basis,
             label='Basis', color='yellow', alpha=0.5)
    plt.fill_between(financial_data.index, upper, lower,
                     label='Background', color='lightblue', alpha=0.7)
    plt.fill_between(financial_data.index, upper, basis, where=(
        upper > basis), label='Buy Zone', color='green', alpha=0.7)
    plt.fill_between(financial_data.index, lower, basis, where=(
        lower < basis), label='Sell Zone', color='red', alpha=0.7)

    # plot the data with the offset
    plt.plot(financial_data.index,
             financial_data['Close'], label='Close Price', color='blue')

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('VOLD Ratio and Bollinger Bands')
    plt.legend()
    plt.grid(True)

    if record_to_plot is not None:
        plt.show()
    else:
        return vold

    return financial_data
