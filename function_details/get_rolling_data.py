import pandas as pd
import numpy as np


def get_rolling_data(df, rolling_dict, limit_dict, tag_list, exception_list, run_tag, dol_tag):
    print("Get rolling data")
    print(df.columns)
    print(df)
    for tag in tag_list:
        if tag not in exception_list:
            rolling_value = rolling_dict[tag]
            limit_value = limit_dict[tag]

            # Sort the DataFrame
            df.sort_values([run_tag, dol_tag], inplace=True)
            # Create a new column for cumulative average
            df[tag + "_rolling"] = 0.0

            # Calculate cumulative average
            # current_run = None

            # Create a mask to identify rows where 'current_run' changes
            # mask = df['run'].shift() != df['run']

            # Initialize variables
            running_sum = np.zeros(len(df))
            running_count = np.zeros(len(df))

            # Compute running sum and count
            running_sum += df[tag]
            running_count += 1

            # Compute cumulative average
            # breakpoint()
            df[tag + "_rolling"] = np.where(df[dol_tag] <= limit_value, running_sum.cumsum() / running_count.cumsum(), np.nan)

            # Compute previous 15-day average for rows where 'days' > 15
            df[tag + "_rolling"].mask(df[dol_tag] > limit_value, df[tag].rolling(window=rolling_value).mean(), inplace=True)

    return df


def run_script():
    input_data = pd.read_csv(r"D:\AutoML-Outage\input\data_rolling.csv").dropna()
    features_df = pd.read_csv(r"D:\AutoML-Outage\config\get_rolling.csv").dropna()
    rolling_dict = dict(features_df[['tag_name', 'rolling_window']].values)
    limit_dict = dict(features_df[['tag_name', 'limit']].values)
    tag_list = features_df['tag_name'].dropna().to_list()
    exception_list = features_df['tag_exception'].dropna().to_list()
    run_tag = str(features_df['run_tag'].values[0])
    dol_tag = str(features_df['dol_tag'].values[0])
    result_df = get_rolling_data(input_data, rolling_dict, limit_dict, tag_list, exception_list, run_tag, dol_tag)
    result_df.to_csv(r"D:\AutoML-Outage\output\output_rolling_data.csv")
    return result_df


# run_script()
