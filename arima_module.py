import pandas_ta as pa
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

from pmdarima import auto_arima


def arima_model(financial_data: pd.DataFrame, record_to_plot: int = 2000, fig: go.Figure = None, dates=None) -> go.Figure:

    def support_resistance(variable, fig=fig, record_to_plot=record_to_plot, financial_data=financial_data, dates=dates):
        financial_data = financial_data[:record_to_plot][variable]

        df_train = financial_data[:int(0.80*(len(financial_data)))]
        df_test = financial_data[int(0.20*(len(financial_data))):]

        auto_arima_ = auto_arima(df_train, stepwise=False, seasonal=True)

        forecast_test_auto = auto_arima_.predict(n_periods=len(df_test))

        financial_data['forecast_auto'] = [None] * \
            len(df_train) + list(forecast_test_auto)

        model = ExponentialSmoothing(
            df_train, trend='mul', seasonal='mul', seasonal_periods=10).fit()
        best_model = model.forecast(len(df_test))

        financial_data['forecast_smoothing'] = [
            None]*len(df_train) + list(best_model)

        fig.add_trace(go.Scatter(x=financial_data.index,
                      y=financial_data['forecast_smoothing'], name='Forecast Smothing',    line=dict(color='blue', width=1)))

    support_resistance('Close')
    support_resistance('Open')
