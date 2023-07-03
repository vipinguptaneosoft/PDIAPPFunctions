import numpy as np
from scipy import stats
import pandas as pd


def get_slopes(df,tag_list, exception_list, limit_dict, run_tag, dol_tag, x_dict, y_dict):
    print("calculating the slopes")
    print(tag_list, exception_list, limit_dict, run_tag, dol_tag, x_dict, y_dict)
    print(df)
    # Sort the DataFrame by 'run' and 'days' columns
    df.sort_values([run_tag, dol_tag], inplace=True)
    x_value = None
    y_value = None
    limit_value = None
    # Calculate slopes using iterrows
    for tag in tag_list:
        if tag not in exception_list:
            df[tag + '_slope'] = np.nan
            # breakpoint() 
            # rolling_value = rolling_dict[tag]
            x_value = x_dict[tag]
            y_value = y_dict[tag]
            limit_value = limit_dict[tag]

        for index, row in df.iterrows():
            run = row[run_tag]
            day = row[dol_tag]

            if day <= limit_value:
                current_data = df[(df[run_tag] == run) & (df[dol_tag] <= day)]
            else:
                current_data = df[(df[run_tag] == run) & (df[dol_tag] > (day - limit_value)) & (df[dol_tag] <= day)]

            x_values = current_data[x_value].values
            y_values = current_data[y_value].values

            # Remove NaN values
            valid_indices = np.logical_and(~np.isnan(x_values), ~np.isnan(y_values))
            x_values = x_values[valid_indices]
            y_values = y_values[valid_indices]

            if len(x_values) < 2:
                slope = np.nan
            else:
                slope, _, _, _, _ = stats.linregress(x_values, y_values)

            df.loc[index, tag + '_slope'] = slope
    return df, run_tag


# Sort the DataFrame by 'run' and 'days' columns


# def run_script():
#     input_data = pd.read_csv(r"D:\AutoML-Outage\test\test data\data_rolling.csv")
#     features_df = pd.read_csv(r"D:\AutoML-Outage\test\test data\slopes_config.csv")
#     # rolling_dict = dict(features_df[['tag_name', 'rolling_window']].values)
#     limit_dict = dict(features_df[['tag_name', 'limit']].values)
#     tag_list = features_df['tag_name'].dropna().to_list()
#     exception_list = features_df['tag_exception'].dropna().to_list()
#     run_tag = str(features_df['run_tag'].values[0])
#     dol_tag = str(features_df['dol_tag'].values[0])
#     x_dict = dict(features_df[['tag_name', 'x_value']].values)
#     y_dict = dict(features_df[['tag_name', 'y_value']].values)
#     result_df = get_slopes(input_data, tag_list, exception_list, limit_dict, run_tag, dol_tag, x_dict, y_dict)
#     result_df.to_csv(r"D:\AutoML-Outage\output\output_slopes_data_test.csv")
#     return result_df
#
#
# run_script()
