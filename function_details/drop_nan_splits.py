import os
import pandas as pd
from sklearn.model_selection import train_test_split

# List of columns to check for values

#features_df = pd.read_csv(r"D:\AutoML-Outage\config\split_drop_config.csv")
#column_folder_dict = dict(features_df[['folder_name', 'listofcols']].values)

# Folder path
ti_folder_path = './function_details/TI/'


# Function to delete rows with specified values in given columns
def delete_rows_with_values(df, y_column):
    df = df.dropna(subset=y_column, how='any')
    return df


# Function to merge X and y files
def merge_files(subfolder_path):
    X_train = pd.read_csv(os.path.join(subfolder_path, "X_train.csv"))
    y_train = pd.read_csv(os.path.join(subfolder_path, "y_train.csv"))
    X_test = pd.read_csv(os.path.join(subfolder_path, "X_test.csv"))
    y_test = pd.read_csv(os.path.join(subfolder_path, "y_test.csv"))

    merged_train = pd.concat([X_train, y_train], axis=1)
    merged_test = pd.concat([X_test, y_test], axis=1)

    return merged_train, merged_test


# Function to split merged data into X and y
def split_data(merged_train, merged_test):
    X_train = merged_train.iloc[:, :-1]
    y_train = merged_train.iloc[:, -1]

    X_test = merged_test.iloc[:, :-1]
    y_test = merged_test.iloc[:, -1]

    return X_train, X_test, y_train, y_test


# Iterate through subfolders in the "TI" folder
def remove_nan_on_y(column_folder_dict):
    print(column_folder_dict)
    folder_list = []
    for subfolder in os.listdir(ti_folder_path):
        print(subfolder)
        subfolder_path = os.path.join(ti_folder_path, subfolder)
        print(column_folder_dict)
        try:
            column_y_name = column_folder_dict[subfolder]
        except KeyError:
            continue

        # Only process if the item is a subfolder
        if os.path.isdir(subfolder_path):
            print("Processing subfolder:", subfolder)

            # Merge X_train, y_train, X_test, and y_test files
            merged_train, merged_test = merge_files(subfolder_path)

            # Apply deletion of NaN values on merged train and test DataFrames
            merged_train = delete_rows_with_values(merged_train, column_y_name)
            merged_test = delete_rows_with_values(merged_test, column_y_name)

            # Split merged data into X_train, X_test, y_train, and y_test
            X_train, X_test, y_train, y_test = split_data(merged_train, merged_test)

            # Store cleaned files in a new folder within the same "TI" directory
            # cleaned_data_folder = os.path.join(ti_folder_path, subfolder + "_cleaned_data")
            # os.makedirs(cleaned_data_folder, exist_ok=True)
            #
            # X_train.to_csv(os.path.join(cleaned_data_folder, "X_train.csv"), index=False)
            # y_train.to_csv(os.path.join(cleaned_data_folder, "y_train.csv"), index=False)
            # X_test.to_csv(os.path.join(cleaned_data_folder, "X_test.csv"), index=False)
            # y_test.to_csv(os.path.join(cleaned_data_folder, "y_test.csv"), index=False)

            X_train.to_csv(os.path.join(subfolder_path, "X_train.csv"), index=False)
            y_train.to_csv(os.path.join(subfolder_path, "y_train.csv"), index=False)
            X_test.to_csv(os.path.join(subfolder_path, "X_test.csv"), index=False)
            y_test.to_csv(os.path.join(subfolder_path, "y_test.csv"), index=False)

            folder_list.append(column_y_name)
    print(folder_list)
    return folder_list


#remove_nan_on_y(column_folder_dict)
