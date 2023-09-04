import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_qqe_rsi_trailing_stop(financial_data: pd.DataFrame, record_to_plot: int = None, length=5, factor=4.236, smooth=60):
    # Read financial data
    financial_data = financial_data[:record_to_plot]
    # make column named signal
    financial_data["signal"] = 0
    close_prices = financial_data['Close'].values

    # Calculate RSI
    delta = np.diff(close_prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.mean(gain[:length])
    avg_loss = np.mean(loss[:length])

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    for i in range(length, len(close_prices)):
        delta = close_prices[i] - close_prices[i - 1]
        gain = max(delta, 0)
        loss = -min(delta, 0)

        avg_gain = ((length - 1) * avg_gain + gain) / length
        avg_loss = ((length - 1) * avg_loss + loss) / length

        rs = avg_gain / avg_loss
        rsi = np.append(rsi, 100 - (100 / (1 + rs)))

    # Calculate Trailing Stop
    # Calculate the difference between consecutive RSI values
    rsi_diff = np.diff(rsi)

    crossover = np.where(rsi > 0, 1, 0)
    crossunder = np.where(rsi < 0, 1, 0)

    close_prices = close_prices[:-1]
    crossunder = crossunder[:-1]

    ts = np.zeros_like(rsi)  # Initialize ts with zeros
    crossover = crossover[:-1]
    for i in range(1, len(rsi)-1):
        if crossover[i]:
            ts[i] = rsi[i] - np.abs(rsi_diff[i]) * factor
        elif crossunder[i]:
            ts[i] = rsi[i] + np.abs(rsi_diff[i]) * factor
        else:
            if rsi[i] > ts[i - 1]:
                ts[i] = max(rsi[i] - np.abs(rsi_diff[i]) * factor, ts[i - 1])
            else:
                ts[i] = min(rsi[i] + np.abs(rsi_diff[i]) * factor, ts[i - 1])

    for i in range(1, len(ts)):
        ts[i] = ts[i] / 100 * close_prices[i] + (1 - ts[i] / 100) * ts[i - 1]
        rsi[i] = rsi[i] / 100 * close_prices[i] + \
            (1 - rsi[i] / 100) * rsi[i - 1]

    # Smooth RSI
    smoothed_rsi = np.convolve(rsi, np.ones(smooth)/smooth, mode='valid')
    smoothed_rsi = np.concatenate(
        (rsi[:smooth-1], smoothed_rsi))  # Preserve original length
    
    # start plotting
    plt.figure(figsize=(10, 6))
    plt.plot(close_prices[smooth:], label='Close Price')
    last_signal = None
    for i in range(1, len(smoothed_rsi)):
        # if the smoothed rsi is greater than the trailing stop, buy
        if last_signal == None:
            if smoothed_rsi[i] > ts[i] and i+smooth < len(close_prices):
                plt.plot(i, close_prices[i+smooth], marker='o', color='red')
                last_signal = 'buy'
                financial_data["signal"][i] = 2
            else:
                plt.plot(i, close_prices[i+smooth], marker='o', color='green')
                last_signal = 'sell'
                financial_data["signal"][i] = 1
        if smoothed_rsi[i] > ts[i] and i+smooth < len(close_prices):
            if last_signal != 'buy':
                plt.plot(i, close_prices[i+smooth], marker='o', color='red')
                last_signal = 'buy'
                financial_data["signal"][i] = 2
        # if the smoothed rsi is less than the trailing stop, sell
        if smoothed_rsi[i] < ts[i] and i+smooth < len(close_prices):
            if last_signal != 'sell':
                plt.plot(i, close_prices[i+smooth], marker='o', color='green')
                last_signal = 'sell'
                financial_data["signal"][i] = 1

    # Increase smoothness of the trailing stop

    # Plot the results
    if record_to_plot is not None:
        plt.plot(smoothed_rsi[smooth+2:], label='Trailing Stop')
        plt.legend(loc='upper left')
        plt.show()

    return financial_data

# Example usage:
# Assuming you have a Pandas DataFrame 'financial_data' with a 'close' column
# and you want to plot the indicator for record 0:
# rsi_values, ts_values = calculate_qqe_rsi_trailing_stop("data/EURGBP_Candlestick_4_Hour_BID_23.07.2013-22.07.2023.csv", record_to_plot=0)
