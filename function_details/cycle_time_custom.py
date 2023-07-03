import pandas as pd
import numpy as np
from datetime import timedelta
import re


def eval_formula(formula: str):
    rename_dict = {"{": "df['", "}": "']"}
    regx_min_max = re.compile(r"(min|max|AVERAGE)\((.+?)\)")
    regx = re.compile(r"\{(.+?)\}")
    rep = {'or': 'logical_or(', 'and': 'logical_and('}
    pattern = "|".join(rep.keys())
    pattern = re.compile(fr"({pattern})\(")

    formula = pattern.sub(lambda m: m.group(1).replace(m.group(1), rep[m.group(1)]), formula)
    formula = re.sub(r"(np\.)?(where|isnan|power|exp|logical_or|logical_and|abs)\(", r"np.\2(",
                     formula)  # add np. to where
    formula = regx_min_max.sub(
        lambda g: f"df[{regx.findall(g.group(2))}].{g.group(1).replace('AVERAGE', 'mean')}(axis=1)", formula)

    for key, val in rename_dict.items():
        formula = formula.replace(key, val)
    return formula


def get_cycle_time(input_df, status_tag, condition_dict, cycle_tag_dict, time_unit_dict, pattern_dict, round_dict,
                   freq_dict):
    input_df.reset_index(inplace=True)
    print("calculating cycle time and dol's")
    input_df['time'] = pd.to_datetime(input_df['time'], dayfirst=True, errors='coerce')
    input_df['time'] = input_df['time'].dt.strftime('%Y-%m-%d %H:%M')
    input_df.set_index('time', inplace=True)
    input_df.index = pd.to_datetime(input_df.index)
    input_data = input_df.copy(deep=True)
    input_data.reset_index(inplace=True)
    for tag in status_tag:
        freq_min = freq_dict[tag]
        formula = condition_dict[tag]
        formula = eval_formula(formula)
        result_tag = 'result_' + tag
        cycle_tag = cycle_tag_dict[tag]
        time_unit = time_unit_dict[tag]
        pattern = pattern_dict[tag]
        round_flag = round_dict[tag]

        # if its drum then cycletime hours else for furnace its days online
        df = input_data.copy(deep=True)

        # define the conditions to filter the dataframe
        conditions = [
            eval(formula),
        ]

        # define the corresponding values for each condition
        values = [
            1,
        ]

        # create a new column in the dataframe with the calculated values
        df[result_tag] = np.select(conditions, values, default=0)

        # find the index where the result switches from 0 to 1 and vice versa
        if not df[df[result_tag] == 1].empty:
            switch_on_index = df[df[result_tag] == 1].index[0]
        else:
            switch_on_index = -1

        if not df[df[result_tag] == 0].empty:
            switch_off_index = df[df[result_tag] == 0].index[-1]
        else:
            switch_off_index = -1

        # create a mask to identify the rows where the result is on
        mask = df[result_tag].eq(1)

        # create a new 'diff' column in the dataframe and fill it with the cumulative difference
        if pattern == 'reset':
            df[cycle_tag] = 0
            cumulative_sum = 0
            for i, value in df.iterrows():
                if i >= switch_on_index:
                    if mask[i]:
                        df.loc[i, cycle_tag] = cumulative_sum
                        if time_unit == 'hrs':
                            cumulative_sum += freq_min / 60
                        else:
                            cumulative_sum += freq_min / 1440
                    elif i <= switch_off_index:
                        cumulative_sum = 0
        if pattern == 'noreset':
            df[cycle_tag] = 0
            if time_unit == 'hrs':
                df.loc[switch_on_index:, cycle_tag] = mask[switch_on_index:].cumsum().sub(1).mul(freq_min / 60)
            else:
                df.loc[switch_on_index:, cycle_tag] = mask[switch_on_index:].cumsum().sub(1).mul(freq_min / 1440)
            df.loc[df[result_tag].eq(0), cycle_tag] = 0

        df.drop(result_tag, inplace=True, axis=1)
        if round_flag == 'no':
            input_data[cycle_tag] = df[cycle_tag].values
        else:
            input_data[cycle_tag] = np.floor(df[cycle_tag].values)
    input_data.sort_index(ascending=False, inplace=True)
    return input_data


# def run_script():
#     #input_data = pd.read_csv(r"D:\AutoML-Outage\test\test data\data_dol.csv")
#     # input_data = pd.read_csv(r"D:\AutoML-Outage\output\check_run_db.csv")
#     input_data = pd.read_csv(r"D:\AutoML-Outage\test\test data\get_run_number_output.csv")
#     features_df = pd.read_csv(r"D:\AutoML-Outage\test\test data\features_cycletime.csv")
#     status_tags = features_df['status_tags'].to_list()
#     condition_dict = dict(features_df[['status_tags', 'condition']].values)
#     cycle_tag_dict = dict(features_df[['status_tags', 'cycle_output_tags']].values)
#     time_unit_dict = dict(features_df[['status_tags', 'time_unit']].values)
#     pattern_dict = dict(features_df[['status_tags', 'pattern']].values)
#     round_dict = dict(features_df[['status_tags', 'round']].values)
#     freq_dict = dict(features_df[['status_tags', 'freq_min']].values)
#     result_df = get_cycle_time(input_data, status_tags, condition_dict, cycle_tag_dict, time_unit_dict, pattern_dict,
#                                round_dict, freq_dict)
#     result_df.to_csv(r'D:\AutoML-Outage\output\check_cycle_db_test.csv')
#     return result_df
#
#
# run_script()
