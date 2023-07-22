# In file S&P500.csv, the first column is the date,
# Date: 07/12/2023 ,Open,High,Low,Close

import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import plotly.graph_objects as go
import os
import matplotlib.pyplot as plt
import pandas as pd
from initial_visualisation import plot_candlestick_data, plot_candlestick_data_2, plot_nasdaq
from xg_boost import xg_boost_pred
from support_resistance import detection_support_resistance
from trendline_detection import trendline_detect
def S_and_P_500():
    data = pd.read_csv("data\S&P500.csv")
    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=["timestamp", "Open", "High", "Low", "Close"])

    df["Open"] = df["Open"].str.replace(",", "").astype(float)
    df["High"] = df["High"].str.replace(",", "").astype(float)
    df["Low"] = df["Low"].str.replace(",", "").astype(float)
    df["Close"] = df["Close"].str.replace(",", "").astype(float)

    # Convert the Date column to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%m/%d/%Y")

    # Sort the DataFrame by Date
    df.sort_values("timestamp", inplace=True)
    plot_candlestick_data(df)


def google_data():
    files = [
        "data\GOOG_1hour_sample.csv",
        "data\GOOG_1day_sample.csv",
        "data\GOOG_1min_sample.csv",
        "data\GOOG_5min_sample.csv",
        "data\GOOG_30min_sample.csv",
    ]
    for file in files:
        data = pd.read_csv(file)
        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close","volume"])

        # Parse the timestamp column as datetime and set it as the index
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values("timestamp", inplace=True)
        x = df['timestamp']
        
        plot_candlestick_data_2(df)
        
def nasdaq_data():

    folder_path = 'data_nasdaq'  # Replace with the actual folder path

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the current item is a file
        if os.path.isfile(file_path):
            # Process the file or perform desired operations
            data = pd.read_csv(file_path)
            
            
            df = pd.DataFrame(data, columns=['Date', 'Close/Last', 'Volume', 'Open', 'High', 'Low'])
        
            # Format the Date column as datetime
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
            df.set_index('Date', inplace=True)

            # Rename the column for compatibility with plot_candlestick_data function
            df.rename(columns={'Close/Last': 'Close'}, inplace=True)
            
            
            #plot the data
            plot_nasdaq(df,filename)
            
def plot_yearly(filename):
    data = pd.read_csv(filename)
            
            
    df = pd.DataFrame(data, columns=['Date', 'Close/Last', 'Volume', 'Open', 'High', 'Low'])

    # Format the Date column as datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df.set_index('Date', inplace=True)
    #sort the data by date
    df.sort_values("Date", inplace=True)
    # Rename the column for compatibility with plot_candlestick_data function
    df.rename(columns={'Close/Last': 'Close'}, inplace=True)
    
    company = filename.split("Data_")[1].split(".")[0]
    data_by_year = {}
    for entry in df.index:
        year = entry.year
        if year not in data_by_year:
            data_by_year[year] = []
        data_by_year[year].append(entry)
    
    for year in data_by_year:
        temp_data = df.loc[data_by_year[year]]
        print(type(temp_data))
        
        #Visualisation of the data
        plot_nasdaq(temp_data,company=company,filename=year,covid=False)
        
        #XGBoost prediction of the data which is used incorrectly
        #xg_boost_pred(temp_data,company=company,year=year)

        
    
if __name__ == "__main__":
    #S_and_P_500()
    #google_data()
    #nasdaq_data()
    #plot_yearly("data_nasdaq\HistoricalData_SBUX.csv")
    #detection_support_resistance("data_nasdaq\HistoricalData_SBUX.csv")
    trendline_detect("data_nasdaq\HistoricalData_SBUX.csv")