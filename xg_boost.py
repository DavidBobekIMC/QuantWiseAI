#implement xg_boost model for price-forecasting
#time series prediction for stock prices
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
   #xgboost
from xgboost import XGBRegressor
 
        
def xg_boost_pred(df:pd.DataFrame,company:str,year):
    #data = pd.read_csv("data\GOOG_1hour_sample.csv")
    # Convert the data to a Pandas DataFrame

  
    
    y = df['Close']
    #replace each $ with nothing
    for i in range(len(y)):
        y[i] = y[i].replace('$','')
    
    #x is a time series of the open prices
    x = np.arange(1, len(y)+1, 1)
    
    
    x = x.reshape(-1,1)
    y = y.values.reshape(-1,1)

    y_train, y_test, x_train, x_test = train_test_split(y, x, test_size=0.2, random_state=0)

    
    #xgboost
    xgb = XGBRegressor()
    xgb.fit(x_train, y_train)
    
    y_pred = xgb.predict(x_test)
    
    #convert from numpy.ndarray so that we can plot

    y_pred = y_pred.flatten()
    
    #to float32
    y_test = y_test.astype('float32')
    #plot the results
    plt.figure(figsize=(16,8))
    plt.plot(y_test, label='Close')
    plt.plot(y_pred, label='Predicted Close')
    plt.title('XGBoost for '+company+' in '+str(year))
    plt.legend()
    plt.show()
    statistics(y_test,y_pred)
    
def statistics(y_test,y_pred):
    y_pred = y_pred.flatten()
    y_test = y_test.astype('float32')
    #mean absolute error
    mae = mean_absolute_error(y_test, y_pred)
    print('MAE: %.3f' % mae)
    #mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print('MSE: %.3f' % mse)
    #root mean squared error
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print('RMSE: %.3f' % rmse)
    #r2 score
    r2 = r2_score(y_test, y_pred)
    print('R2: %.3f' % r2)
    #mean absolute percentage error
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    print('MAPE: %.3f' % mape)