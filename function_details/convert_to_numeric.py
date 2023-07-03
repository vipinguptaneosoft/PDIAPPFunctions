import pandas as pd
import os

DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\data\\"
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\config\\"
if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
PYTHON_FILE = os.path.basename(__file__)
CONFIG_FILE = [f for f in os.listdir(CONFIG_PATH) if f.startswith(PYTHON_FILE[:-3])]


def convert_to_numeric(df):
    data = pd.read_csv(DATA_PATH + df)
    config = pd.read_csv(CONFIG_PATH + CONFIG_FILE[0])

    columns_exluded = config['exclude'].dropna().to_list()
    if 'time' not in columns_exluded:
        columns_exluded.append('time')
    data.loc[:,~data.columns.isin(columns_exluded)] = data.loc[:,~data.columns.isin(columns_exluded)].apply(pd.to_numeric, errors='coerce')
    data.to_csv(DATA_PATH + CONFIG_FILE[0],index=False)
    return 

if __name__=="__main__":
    convert_to_numeric("test_data.csv")
