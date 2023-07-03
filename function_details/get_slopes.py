import numpy as np
from scipy import stats
import pandas as pd
import time


def get_slopes(data, row, run_tag, dol_tag, limit_value, x_value, y_value):
    start_time = time.now()
    # Sort the DataFrame by 'run' and 'days' columns
    data.sort_values([run_tag, dol_tag], inplace=True)

    # Calculate slopes using iterrows

    run = row[run_tag]
    day = row[dol_tag]

    if day <= limit_value:
        current_data = data[(data[run_tag] == run) & (data[dol_tag] <= day)]
    else:
        current_data = data[(data[run_tag] == run) & (data[dol_tag] > (day - limit_value)) & (data[dol_tag] <= day)]

    x_values = current_data[x_value].values
    y_values = current_data[y_value].values

    if len(x_values) < 2:
        slope = np.nan
    else:
        slope, _, _, _, _ = stats.linregress(x_values, y_values)
    print("GET SLOPES")
    print(time.now()-start_time)
    return slope


# Sort the DataFrame by 'run' and 'days' columns


def run_script():
    input_data = pd.read_csv(r"D:\AutoML-Outage\input\data_slopes.csv").dropna()
    features_df = pd.read_csv(r"D:\AutoML-Outage\config\slopes_config.csv")
    # rolling_dict = dict(features_df[['tag_name', 'rolling_window']].values)
    limit_dict = dict(features_df[['tag_name', 'limit']].values)
    tag_list = features_df['tag_name'].dropna().to_list()
    exception_list = features_df['tag_exception'].dropna().to_list()
    run_tag = str(features_df['run_tag'].values[0])
    dol_tag = str(features_df['dol_tag'].values[0])
    x_value = str(features_df['x_value'].values[0])
    y_value = str(features_df['y_value'].values[0])

    for tag in tag_list:
        if tag not in exception_list:
            input_data[tag + '_slope'] = np.nan
            # rolling_value = rolling_dict[tag]
            limit_value = limit_dict[tag]
            for index, row in input_data.iterrows():
                slope = get_slopes(row, input_data, run_tag, dol_tag, limit_value, x_value, y_value)
                input_data.loc[index, tag + '_slope'] = slope
    input_data.to_csv(r"D:\AutoML-Outage\output\output_slopes_data.csv")
    return input_data


# run_script()
