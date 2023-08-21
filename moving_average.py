import pandas_ta as pa
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


def moving_average(financial_data: pd.DataFrame, record_to_plot: int = 2000, fig: go.Figure = None, dates=None):
    # rename column from Close/Last to Close

    financial_data.rename(columns={"Close/Last": "Close"}, inplace=True)

    for date in dates:
        financial_data[f"MA{date}"] = pa.ema(financial_data.Close, length=date)

    # financial_data["MA7"] = pa.sma(financial_data.Close, length=7)
    # financial_data["MA15"] = pa.sma(financial_data.Close, length=15)
    # financial_data["MA21"] = pa.sma(financial_data.Close, length=21)

    # financial_data["MA60"] = pa.ema(financial_data.Close, length=60)
    # financial_data["MA120"] = pa.ema(financial_data.Close, length=120)
    financial_data.tail(10)

    def mysig(x, prev):
        # dates is a list of dates and we want to check if they cross the moving average
        dates.sort()
        shortest = dates[0]
        longest = dates[-1]

        if x[f"MA{shortest}"] > x[f"MA{longest}"] and prev == -1:
            prev = 1
            print("buy")
            return 1, prev
        elif x[f"MA{shortest}"] < x[f"MA{longest}"] and prev == 1:
            prev = -1
            print("sell")
            return -1, prev
        else:
            return 0, prev

    previous = 1
    for index, row in financial_data.iterrows():
        signal, previous = mysig(row, prev=previous)  # Call mysig for each row

        financial_data.at[index, "signal"] = signal
        if signal == 1:
            fig.add_annotation(
                x=index,
                y=row["Close"],
                text="✅",  # Unicode arrow pointing upwards as a buy signal
                showarrow=True,
                arrowhead=0,  # No arrowhead
                font=dict(size=20),  # Adjust font size as needed
            )
        elif signal == -1:
            fig.add_annotation(
                x=index,
                y=row["Close"],
                text="❌",  # Unicode arrow pointing downwards as a sell signal
                showarrow=True,
                arrowhead=0,  # No arrowhead
                font=dict(size=20),  # Adjust font size as needed
            )
    dfpl = financial_data[:record_to_plot]

    for date in dates:
        fig.add_trace(go.Scatter(
            x=dfpl.index, y=dfpl[f"MA{date}"], mode='lines', name=f'MA{date}'))
        # if signal is 1 then show a green arrow

    # how many signals were there
    print("There were", len(
        financial_data[financial_data["signal"] == 1]), "buy signals")
    print("There were", len(
        financial_data[financial_data["signal"] == -1]), "sell signals")

    # day one
    print("day one", financial_data.iloc[0].at_time)
    # day last
    print("day last", financial_data.iloc[-1].at_time)

    # days where the signal was 1 date
    buy_dates = []
    for index, row in financial_data.iterrows():
        if row["signal"] == 1:
            date = row.values[0]
            position = financial_data.index.get_loc(index)
            buy_dates.append(position)
    print("days where the signal was 1", buy_dates)

    # days where the signal was -1 date
    sell_dates = []
    for index, row in financial_data.iterrows():
        if row["signal"] == -1:
            date = row.values[0]
            position = financial_data.index.get_loc(index)
            sell_dates.append(position)
    print("days where the signal was -1", sell_dates)

    return dfpl
