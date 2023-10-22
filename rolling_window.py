import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# Checks if there is a local peak detected at the current index

def rolling_window(financial_data:  pd.DataFrame, record_to_plot: int=None):
    financial_data = financial_data[:record_to_plot]
    financial_data['signal'] = 0
    def detect_local_peak(data: np.array, curr_index: int, order: int) -> bool:
        if curr_index < order * 2 + 1:
            return False

        peak_detected = True
        k = curr_index - order
        v = data[k]
        for i in range(1, order + 1):
            if data[k + i] > v or data[k - i] > v:
                peak_detected = False
                break

        return peak_detected

    # Checks if there is a local valley detected at the current index


    def detect_local_valley(data: np.array, curr_index: int, order: int) -> bool:
        if curr_index < order * 2 + 1:
            return False

        valley_detected = True
        k = curr_index - order
        v = data[k]
        for i in range(1, order + 1):
            if data[k + i] < v or data[k - i] < v:
                valley_detected = False
                break

        return valley_detected


    def find_extremes(data: np.array, order: int):
        # Rolling window local peaks and valleys
        peaks = []
        valleys = []
        for i in range(len(data)):
            if detect_local_peak(data, i, order):
                peak = [i, i - order, data[i - order]]
                peaks.append(peak)

            if detect_local_valley(data, i, order):
                valley = [i, i - order, data[i - order]]
                valleys.append(valley)

        return peaks, valleys



    financial_data['date'] = pd.to_datetime(
    financial_data['date'], format='%d.%m.%Y %H:%M:%S.%f')
    financial_data = financial_data.set_index('date')

    #financial_data = financial_data[:200]

    detected_peaks, detected_valleys = find_extremes(financial_data['Close'].to_numpy(), 5)

    idx = financial_data.index
    
    last_signal = 0
    for i in range(len(financial_data)):
        financial_data['signal'][i] = 0
        for peak in detected_peaks:
            if i == peak[0]:
                if last_signal != 1:
                    plt.scatter(
                        idx[i], financial_data['Low'][i], c='red', label='Sell', linewidth=1)
                    last_signal = 1
                    financial_data['signal'][i] = 1
                    continue
        for valley in detected_valleys:
            if i == valley[0]:
                if last_signal != 2:
                    plt.scatter(
                        idx[i], financial_data['Low'][i], c='lime', label='Buy', linewidth=1)
                    last_signal = 2
                    financial_data['signal'][i] = 2
                    continue
        
        
    plt.plot(idx, financial_data['Close'])
    plt.show()
    return financial_data


rolling_window("../data/EURGBP_Candlestick_4_Hour_BID_23.07.2013-22.07.2023.csv", 200)