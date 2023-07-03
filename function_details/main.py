from dataclasses import dataclass, field
from typing import List, Dict, Union
from pathlib import Path
import os
import json
from operator import methodcaller
import traceback
import sys

import pandas as pd
import numpy as np


# input file and json file path
cwd = Path(__file__).cwd()
csv_path = cwd / 'inputs.xlsx'

def print_exception(exc):
    if hasattr(exc, 'message'):
        print("Exception " + str(exc.message))
    exec_type, exec_value, tb_obj = sys.exc_info()
    formated_tb = traceback.format_tb(tb_obj)
    for line in formated_tb:
        lst = line.split('\n')
        if (line.find('site-package') == -1) & (line.find('_libs') == -1):
            print(f"{lst[0].strip()}")
    print(f"{exec_type.__name__}: {exec_value}")


@dataclass(frozen=True)
class InputTagDetails:
    pi_tag: str
    tag_alias: str
    default_value: str
    default_value_condition: str

    @classmethod
    def json_to_obj(cls, input_tag_list: List[Dict[str, str]]) -> List['InputTagDetails']:
        input_tags = [InputTagDetails(**tag) for tag in input_tag_list]
        return input_tags
    

def fetch_input_data(csv_path: Path) -> pd.DataFrame:
    return pd.read_excel(csv_path)

def set_def_val(tag_details: List['InputTagDetails'], input_df: pd.DataFrame) -> pd.DataFrame:
    replace_dict = {'{': "input_df['", '}': "']"}
    for tag in tag_details:
        condition = tag.default_value_condition
        value = tag.default_value
        is_special_case = False
        match tag:
            case InputTagDetails(_, tag_alias, _, default_value_condition) if pd.isnull(default_value_condition):
                condition = f"np.isnan({'{'+ tag_alias +'}'})"
            case InputTagDetails(_, tag_alias, _, default_value_condition) if condition.startswith(('!', '>', '<', '=')):
                condition = f"{'{'+ tag_alias + '}'}{condition}"
            case InputTagDetails(_, _, "backfill" | "forwardfill", _):
                value = 'np.nan'
                if tag.default_value.lower == 'backfill':
                    is_special_case = methodcaller('bfill')
                else:
                    is_special_case = methodcaller('fill')
            case _:
                pass
        
        default_cond = f"np.where({condition}, {value}, {'{'+tag.tag_alias+'}'})"

        for key, val in replace_dict.items():
            default_cond = default_cond.replace(key, val)

        try:
            input_df[tag.tag_alias] = eval(default_cond)
            if is_special_case:
                input_df[tag.tag_alias] = is_special_case(input_df[tag.tag_alias])
        except Exception as e:
            print_exception(e)
        
        return input_df
    
def get_input_data(csv_path: Path, json_data: List[Dict[str, Union[str, float, int]]]) -> pd.DataFrame:
    print(json_data)
    input_df = fetch_input_data(csv_path)
    rename_dict = {obj['pi_tag']: obj['tag_alias'] for obj in json_data}
    input_df.rename(columns=rename_dict, inplace=True)
    tag_details = InputTagDetails.json_to_obj(json_data)
    input_df = set_def_val(tag_details, input_df)
    return input_df


if __name__ == "__main__":
    with open('tag_details.json', 'r') as file:
        json_data = json.load(file)

    input_df = get_input_data(csv_path, json_data)
