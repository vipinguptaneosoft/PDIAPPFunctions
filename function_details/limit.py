import pandas as pd
import numpy as np


def get_limit_flags(df, min_dict, max_dict, limit_tags, exception_list, op_dict):
    print("deleting the out of limit tags")
    for tag in limit_tags:
        if tag not in exception_list:
            operation_flag = str(op_dict[tag])
            min_limit = float(min_dict[tag])
            max_limit = float(max_dict[tag])
            mask = (df[tag] < min_limit) | (df[tag] > max_limit)
            if operation_flag == 'nan':
                df[tag] = df[tag].where(~mask, np.nan)
            else:
                df = df[~mask]
    return df


# def run_script():
#     input_data = pd.read_csv(r"D:\AutoML-Outage\input\limit_data.csv")
#     features_df = pd.read_csv(r"D:\AutoML-Outage\config\limit_config.csv")
#     min_dict = dict(features_df[['limit_tags', 'min_limit']].values)
#     max_dict = dict(features_df[['limit_tags', 'max_limit']].values)
#     op_dict = dict(features_df[['limit_tags', 'op_flag']].values)
#     limit_tags = features_df['limit_tags'].to_list()
#     exception_list = features_df['exception_list'].dropna().to_list()
#     result_df = get_limit_flags(input_data, min_dict, max_dict, limit_tags, exception_list, op_dict)
#     result_df.to_csv(r"D:\AutoML-Outage\output\output_limit_data.csv")
#     return result_df
#
#
# run_script()
