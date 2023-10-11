import pandas as pd
import matplotlib.pyplot as plt

def calculate_macd(financial_data:pd.DataFrame,record_to_plot:int,short_window=12, long_window=26, signal_window=9):
    financial_data = financial_data[:record_to_plot]
    # Calculate the short-term exponential moving average (EMA)
    short_ema = financial_data['Close'].ewm(span=short_window, adjust=False).mean()
    
    # Calculate the long-term exponential moving average (EMA)
    long_ema = financial_data['Close'].ewm(span=long_window, adjust=False).mean()
    
    # Calculate the MACD line
    macd = short_ema - long_ema

    financial_data["signal"] = 0
    
    
    # Calculate the signal 
    # 2 = Buy signal
    # 1 = Sell signal
    last_signal = 0
    for i in range(len(financial_data)):
        if i == 792:
            print("i: ", macd[i])
            print("i-1: ", macd[i-1])
        if macd[i] > 0.0015 and macd[i-1] < 0.0015 and last_signal != 2:
            financial_data["signal"][i] = 2
            last_signal = 2
            plt.plot(financial_data.index[i], financial_data["Close"][i], 'o', color='green')
            continue    
            
        if macd[i] < -0.0015 and macd[i-1] > -0.0015 and last_signal != 1:
            financial_data["signal"][i] = 1
            last_signal = 1     
            plt.plot(financial_data.index[i], financial_data["Close"][i], 'o', color='red')
            continue

        
   
    #plt.plot(financial_data.index, macd, label='MACD', color='red')
    plt.plot(financial_data.index, short_ema, label='Short EMA', color='blue')
    plt.plot(financial_data.index, long_ema, label='Long EMA', color='orange')
    plt.plot(financial_data.index, financial_data["Close"], label='Close', color='black')
    
    
    
    plt.legend(loc='upper left')
    plt.show()

    return financial_data    
    


