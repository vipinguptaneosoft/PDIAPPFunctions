import pandas as pd


def get_process_data(df, input_tags, run_dict, limit_dict):
    print("GET process data")
    print(input_tags, run_dict, limit_dict)
    print(df.columns)
    print(df)
    # Group by 'run' and find the maximum value in 'days' for each group
    for dol_tag in input_tags:
        run_tag = run_dict[dol_tag]
        max_days = df.groupby(run_tag)[dol_tag].max()

        # Filter the rows where the maximum 'days' value is less than 10
        df = df[~df[run_tag].isin(max_days[max_days < int(limit_dict[dol_tag])].index)]
    print("output")
    print(df.columns)
    print(df)
    return df


def run_script():
    input_data = pd.read_csv(r"function_details/data_process_runs.csv")
    features_df = pd.read_csv(r"function_details/features_run_process.csv")
    input_tags = features_df['furnace_dol_tags'].to_list()
    run_dict = dict(features_df[['furnace_dol_tags', 'run_tags']].values)
    limit_dict = dict(features_df[['furnace_dol_tags', 'limit']].values)
    result_df = get_process_data(input_data, input_tags, run_dict, limit_dict)
    result_df.to_csv(r'check_process.csv')
    return result_df


# run_script()
