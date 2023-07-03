import pandas as pd


def drop_limit(df, y_column, min_value, max_value, output_name):
    mask = (df[y_column] < int(min_value)) | (df[y_column] > int(max_value))
    df = df[~mask]
    df.to_csv(output_name + ".csv")

    return df

# def drop_limit(file_name):
#     features_df = pd.read_csv(r"./function_details/limit_drop_config.csv")
#     input_data = pd.read_csv(f"./function_details/{file_name}.csv", index_col=[0])
#     column_names = features_df['list_of_columns'].values[0]
#     output_name = features_df['output_name'].dropna().values[0]
#     min_val = features_df['min_value'].dropna().values[0]
#     max_val = features_df['max_value'].dropna().values[0]

#     result_df = drop_limit(input_data, column_names, min_val, max_val, output_name)
#     return result_df
