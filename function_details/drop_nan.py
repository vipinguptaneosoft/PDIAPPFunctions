import pandas as pd


def drop_nan(data_frame, columns, output_name):
    print("DROP NAN")
    print("Input")
    print(data_frame)
    data_frame.dropna(subset=columns, inplace=True)
    data_frame.to_csv(output_name + ".csv")
    print("output")
    print(data_frame)
    return data_frame

def run_config(filename):

    # Remove rows with NaN values in the specified column(s)
    features_df = pd.read_csv(r"./function_details/nan_config.csv")
    input_data = pd.read_csv(f"./function_details/TI/{filename}.csv", index_col=[0])
    column_names = features_df['list_of_columns'].dropna().values[0]
    output_name = features_df['output_name'].dropna().values[0]
    df_cleaned = drop_nan(input_data, column_names, output_name)
    return df_cleaned

