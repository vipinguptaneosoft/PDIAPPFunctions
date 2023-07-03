import pandas as pd
from datetime import timedelta


def remove_toggel(input_data, thresold_dict, tags, freq_dict, toggle_dict):
    print(input_data)
    for tag in tags:
        toggle_flag = int(toggle_dict[tag])
        if toggle_flag == 0:
            min_index = min(input_data.index)
            max_index = max(input_data.index)
            while min_index < max_index:
                if min_index + timedelta(minutes=int(thresold_dict[tag])) in input_data.index:
                    temp_df = input_data[min_index: min_index + timedelta(minutes=int(thresold_dict[tag]))]
                    if float(temp_df[tag].mode().iloc[0]) == 1 and float(
                            temp_df.loc[min(temp_df.index)][tag]) == 1 and float(
                            temp_df.loc[max(temp_df.index)][tag] == 1):
                        input_data.loc[min_index: min_index + timedelta(minutes=int(thresold_dict[tag])), tag] = 1
                    min_index = min_index + timedelta(minutes=freq_dict[tag])
                else:
                    break
        else:
            min_index = min(input_data.index)
            max_index = max(input_data.index)
            while min_index < max_index:
                if min_index + timedelta(minutes=int(thresold_dict[tag])) in input_data.index:
                    temp_df = input_data[min_index: min_index + timedelta(minutes=int(thresold_dict[tag]))]
                    if float(temp_df[tag].mode().iloc[0]) == 0 and float(
                            temp_df.loc[min(temp_df.index)][tag]) == 0 and float(
                        temp_df.loc[max(temp_df.index)][tag] == 0):
                        input_data.loc[min_index: min_index + timedelta(minutes=int(thresold_dict[tag])), tag] = 0
                    min_index = min_index + timedelta(minutes=freq_dict[tag])
                else:
                    break

    return input_data


def run_script():
    input_data = pd.read_csv(r"D:\AutoML-Outage\test\test data\data_calc.csv").dropna(how='all')
    features_df = pd.read_csv(r"D:\AutoML-Outage\test\test data\remove_toggle_config.csv")
    input_data['time'] = pd.to_datetime(input_data['time'], dayfirst=True, errors='coerce')
    input_data['time'] = input_data['time'].dt.strftime('%Y-%m-%d %H:%M')
    input_data.set_index('time', inplace=True)
    input_data.index = pd.to_datetime(input_data.index)
    freq_dict = dict(features_df[['tags', 'time_freq']].values)
    thresold_dict = dict(features_df[['tags', 'threshold_time']].values)
    toggle_dict = dict(features_df[['tags', 'toggle_on']].values)
    tags = features_df['tags'].to_list()
    result_df = remove_toggel(input_data, thresold_dict, tags, freq_dict, toggle_dict)
    result_df.to_csv(r'D:\AutoML-Outage\output\cleaned_data_test.csv')
    return input_data


# run_script()
