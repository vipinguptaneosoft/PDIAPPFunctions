import pandas as pd
from datetime import timedelta
import numpy as np
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


def get_run_number(df, spall_tags, output_dict, if_dict, else_dict):
    print("calculating the run numbers")
    print(df.columns)
    print(df)
    df.reset_index(inplace=True)
    df['time'] = pd.to_datetime(df['time'], dayfirst=True, errors='coerce')
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M')
    df.set_index('time', inplace=True)
    df.index = pd.to_datetime(df.index)

    df.sort_index(axis=0, inplace=True)

    # Iterate over each row in the dataframe
    for tags in spall_tags:
        output_tag = output_dict[tags]
        if_cond = if_dict[tags]
        if_cond = eval_formula(if_cond)
        else_cond = else_dict[tags]
        else_cond = eval_formula(else_cond)
        df['if_cond'] = eval(if_cond)
        df['else_cond'] = eval(else_cond)
        if_values = df['if_cond'].values
        if_values_shifted = np.roll(if_values, 1)
        if_values_shifted[0] = False

        # Check if the previous value was not 1
        sequence_count = np.cumsum((if_values & ~if_values_shifted).astype(int))
        df[output_tag] = sequence_count

        # Update the last value
        last_value = df[tags].values
        last_value_shifted = np.roll(last_value, 1)
        last_value_shifted[0] = 0

        # Assign values based on conditions
        df[output_tag] = np.where(if_values, df[output_tag], df['else_cond'])
        df[output_tag] = df[output_tag].astype(int)

        df.drop(['if_cond', 'else_cond'], axis=1, inplace=True)
    return df


def run_script():
    input_data = pd.read_csv(r"D:\AutoML-Outage\input\input.csv")
    features_df = pd.read_csv(r"D:\AutoML-Outage\test\test data\features_runs_test.csv")
    #input_data = pd.read_csv(r"D:\AutoML-Outage\output\cleaned_data.csv")
    # features_df = pd.read_csv(r"D:\AutoML-Outage\config\features_runs.csv")
    spall_tags = features_df['spall_tags'].to_list()
    run_tag_dict = dict(features_df[['spall_tags', 'run_output_tags']].values)
    thresold_dict = dict(features_df[['spall_tags', 'threshold_time']].values)
    if_dict = dict(features_df[['spall_tags', 'if_condition']].values)
    else_dict = dict(features_df[['spall_tags', 'else_condition']].values)
    result_df = get_runs(input_data, spall_tags, run_tag_dict, if_dict, else_dict)
    result_df.to_csv(r'D:\AutoML-Outage\output\check_run_db.csv')
    return result_df


#run_script()
