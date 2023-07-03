import pandas as pd
import os

def data_split(dataframe, columns, output_name):
    filtered_df = dataframe[columns]
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    FOLDER_PATH = DIRECTORY +"/TI/"
    print(FOLDER_PATH)
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    filtered_df.to_csv(f"{FOLDER_PATH}{output_name}" + ".csv")
    print("Return of DataSplit")
    print(f"{FOLDER_PATH}{output_name}.csv")
    # return f"TI/{output_name}.csv"
    return filtered_df


# Create a sample dataframe
# data = pd.read_csv(r"D:\AutoML-Outage\output\output_slopes_data_test.csv")
# features_df = pd.read_csv(r"D:\AutoML-Outage\config\data_split_config.csv")
# column_names = features_df['columns'].tolist()
# output_name = features_df['output_name'].dropna().values[0]

# result_df = data_split(data, column_names, output_name)
# result_df.to_csv("D:\AutoML-Outage\output\split_data.csv")
