import pandas as pd


def backfill_columns(df, column_names):
    # Sort the dataframe by the time column
    df.sort_values(by='time', inplace=True)

    # Perform backfilling for each specified column
    for column_name in column_names:
        df[column_name].fillna(method='bfill', inplace=True)
    print(df)
    return df


def run_script():
    input_data = pd.read_csv(r"D:\AutoML-Outage\test\test data\data_dol.csv")
    features_df = pd.read_csv(r"D:\AutoML-Outage\config\fill_config.csv")
    features_df.dropna(inplace=True)
    input_tags = features_df['columnstofill'].to_list()
    result_df = backfill_columns(input_data, input_tags)
    result_df.to_csv("D:\AutoML-Outage\output\output_bfill.csv")
    return result_df


# run_script()
