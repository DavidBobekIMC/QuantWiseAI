# In file S&P500.csv, the first column is the date,
# Date: 07/12/2023 ,Open,High,Low,Close
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import pandas as pd
from initial_visualisation import plot_candlestick_data, plot_candlestick_data_2


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
    
if __name__ == "__main__":
    S_and_P_500()
    google_data()
