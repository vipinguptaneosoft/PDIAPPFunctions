import pandas as pd


def get_daily_average(df, run_dict, run_tags):
    print("calculating daily average data")
    print(df)
    output_df = pd.DataFrame()
    time_df = pd.DataFrame()
    df.set_index('time', inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    for run_tag in run_tags:
        df = df[~df[run_tag].isin([0, -1])]
        dol_tag = run_dict[run_tag]
        df = df[df[dol_tag] != 0]
        output_df = df.groupby([run_tag, dol_tag]).mean()
        # output_df = df.groupby([run_tag, dol_tag]).agg(lambda x: x.mean(skipna=True))
        df.reset_index(inplace=True)
        time_df['time'] = df.groupby([run_tag, dol_tag]).min()['time']
        output_df.reset_index(inplace=True)
        output_df['time'] = time_df['time'].values
        output_df.set_index('time', inplace=True)
    print(output_df)
    return output_df

# def run_script():
#     #input_data = pd.read_csv(r"D:\AutoML-Outage\test\test data\data_dol.csv")
#     input_data = pd.read_csv(r"D:\AutoML-Outage\output\check_cycle_db.csv")
#     features_df = pd.read_csv(r"D:\AutoML-Outage\config\get_daily_avg_data.csv")
#     run_dict = dict(features_df[['run_tags', 'days_tag']].values)
#     run_tags = features_df['run_tags'].to_list()
#     result_df = get_daily_average(input_data, run_dict, run_tags)
#     result_df.to_csv(r"D:\AutoML-Outage\output\check_avg_db.csv")
#     return result_df
#
#
# run_script()