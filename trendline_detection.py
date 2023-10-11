import pandas as pd
import numpy as np
import plotly.graph_objects as go

def trendline_detect(financial_data:pd.DataFrame, num_back_candles: int = 70, back_candle_range: int = 50, window_size: int = 7,record_to_plot: int = 2000,fig:go.Figure=None)->pd.DataFrame:
    """_summary_

    Args:
        file_path (str): _description_
        num_back_candles (int, optional): _description_. Defaults to 70. 
        back_candle_range (int, optional): _description_. Defaults to 50.
        window_size (int, optional): _description_. Defaults to 7.
        record_to_plot (int, optional): _description_. Defaults to 2000.

    Returns:
        plotly graph
    """
  

    

    # Candle id is the index of the candle in the dataset that we are currently processing
    candle_id = num_back_candles+back_candle_range

    #data to plot: selection of the data to plot (first 2000 candles by default)
    if record_to_plot > len(financial_data):
        raise ValueError("record_to_plot must be less than the length of the dataset")
    else:
        financial_data = financial_data[:record_to_plot]

    last_signal = 0
    
    financial_data['signal'] = 0
    #initialise the report dataframe 
    report = pd.DataFrame(columns=['candle_id','slope_min','slope_max','intercept_min','intercept_max','dist','xx_min','xx_max','min_vals','max_vals'])
    while candle_id < record_to_plot:
        optimal_num_back_candles = num_back_candles
        slope_diff_threshold = 100
        slope_dist_threshold = 0.05

        for r1 in range(num_back_candles - back_candle_range, num_back_candles + back_candle_range):
            max_vals = np.array([])
            min_vals = np.array([])
            xx_min = np.array([])
            xx_max = np.array([])

            for i in range(candle_id - r1, candle_id + 1, window_size):
                min_vals = np.append(min_vals, financial_data.Low.iloc[i:i + window_size].min())
                xx_min = np.append(xx_min, financial_data.Low.iloc[i:i + window_size].idxmin())
            for i in range(candle_id - r1, candle_id + 1, window_size):
                max_vals = np.append(max_vals, financial_data.High.loc[i:i + window_size].max())
                xx_max = np.append(xx_max, financial_data.High.iloc[i:i + window_size].idxmax())

            slope_min, intercept_min = np.polyfit(xx_min, min_vals, 1)
            slope_max, intercept_max = np.polyfit(xx_max, max_vals, 1)

            dist = (slope_max * candle_id + intercept_max) - (slope_min * candle_id + intercept_min)
            print("dist: ", dist)
            if dist < slope_dist_threshold:  # abs(slope_min - slope_max) < slope_diff_threshold and
                slope_dist_threshold = dist
                optimal_num_back_candles = r1
                slope_min_optimal = slope_min
                slope_max_optimal = slope_max
                intercept_min_optimal = intercept_min
                intercept_max_optimal = intercept_max
                max_vals_optimal = max_vals.copy()
                min_vals_optimal = min_vals.copy()
                xx_min_optimal = xx_min.copy()
                xx_max_optimal = xx_max.copy()

        data_to_plot = financial_data[candle_id - window_size - optimal_num_back_candles - num_back_candles:
                                      candle_id + optimal_num_back_candles]

        adj_intercept_max = (financial_data.High.iloc[xx_max_optimal] - slope_max_optimal * xx_max_optimal).max()
        adj_intercept_min = (financial_data.Low.iloc[xx_min_optimal] - slope_min_optimal * xx_min_optimal).min()


        if (slope_min_optimal > 0):
            color = 'green'
            if last_signal is not 2:
                financial_data['signal'][candle_id] = 2
                last_signal = 2
        else:
            color = 'red'
            if last_signal is not 1:
                financial_data['signal'][candle_id] = 1
                last_signal = 1
                

        fig.add_trace(go.Scatter(x=xx_min_optimal, y=slope_min_optimal * xx_min_optimal + adj_intercept_min,
                                 mode='lines', name='min slope', line=dict(color=color)))
        fig.add_trace(go.Scatter(x=xx_max_optimal, y=slope_max_optimal * xx_max_optimal + adj_intercept_max,
                                 mode='lines', name='max slope', line=dict(color=color)))
        

        report = report._append({'candle_id': candle_id,
                                'slope_min': slope_min_optimal,
                                'slope_max': slope_max_optimal,
                                'intercept_min': adj_intercept_min,
                                'intercept_max': adj_intercept_max,
                                'dist': slope_dist_threshold,
                                'xx_min': xx_min_optimal,
                                'xx_max': xx_max_optimal,
                                'min_vals': min_vals_optimal,
                                'max_vals': max_vals_optimal}, ignore_index=True)
        
        candle_id += optimal_num_back_candles 
        
   
    #save report to csv
    #report.to_csv('report.csv',index=False)

    return financial_data
