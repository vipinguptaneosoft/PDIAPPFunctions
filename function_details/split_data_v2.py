import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def generate_splits():
    data = pd.read_csv(r"function_details/data_minmax.csv")
    features = pd.read_csv(r"function_details/split_config.csv")

    X_columns = features['x_variables'].dropna().to_list()
    Y_columns = features['y_variables'].dropna().to_list()
    config = dict(features[['config', 'config_value']].dropna().values)
    X = data[X_columns]
    total_folder_names = []
    for y in Y_columns:
        Y = data[[y]]
        X_train, X_test, y_train, y_test = train_test_split(X, Y, 
                                                            test_size = float(config['TEST_FRACTION']), 
                                                            random_state = int(config['RANDOM_STATE']), 
                                                            shuffle = config['SHUFFLE'])
        DIRECTORY = os.path.dirname(os.path.realpath(__file__))
        FOLDER_PATH = DIRECTORY +"/TI/" + f"{y}/"
        print(FOLDER_PATH)
        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)
        X_train.to_csv(FOLDER_PATH + "X_train.csv", index=False)
        X_test.to_csv(FOLDER_PATH + "X_test.csv", index=False)
        y_train.to_csv(FOLDER_PATH + "y_train.csv", index=False)
        y_test.to_csv(FOLDER_PATH + "y_test.csv", index=False)
        total_folder_names.append(f"{y}")
        print(X_train)
        print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        print(os.listdir(FOLDER_PATH))
    return total_folder_names

# generate_splits()



