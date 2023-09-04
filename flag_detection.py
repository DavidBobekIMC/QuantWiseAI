import pandas as pd
import matplotlib.pyplot as plt

def flag_detection(csv_filename):
    # Read CSV data into a pandas DataFrame
    df = pd.read_csv(csv_filename)
    df =df[:2000]
    # Calculate moving averages
    df['50MA'] = df['close'].rolling(window=50).mean()
    df['200MA'] = df['close'].rolling(window=200).mean()
    
    # Calculate ATR (Average True Range) for volatility
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=10).mean()  # Adjust window size as needed
    
    # Define a threshold for flag detection based on ATR
    atr_multiplier = 6  # Adjust this value as needed
    
    # Flag detection logic
    flag_indices = []
    for i in range(200, len(df)):
        if df['50MA'][i] > df['200MA'][i]:
            flag_range = df['high'][i-20:i+20].max() - df['low'][i-20:i+20].min()
            price_range = df['close'][i] - df['close'][i-1]
            
            # If the price range is within the threshold of the flag range, then it's a flag
            
            
            if price_range <= atr_multiplier * df['ATR'][i]:
                flag_indices.append(i)
                
                plt.plot(df['date'][i-20:i+20], df['close'][i-20:i+20], label='Flag Pattern', color='r')
    
    # Plotting the data along with detected flag patterns
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['close'], label='Close Price')
    
    # use flag range to plot the flag pattern
    for i in flag_indices:
        plt.plot(df['date'][i-20:i+20], df['close'][i-20:i+20], label='Flag Pattern', color='r')
        
    # Plot moving averages
    plt.plot(df['date'], df['50MA'], label='50MA')
    plt.plot(df['date'], df['200MA'], label='200MA')
        
    # flag range
     
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Dynamic Flag Pattern Detection')
  
    
    # Show the plot
    plt.show()

# Replace 'financial_data.csv' with the actual filename of your CSV data
flag_detection('data/EURGBP_Candlestick_4_Hour_BID_23.07.2013-22.07.2023.csv')