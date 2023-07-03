import pandas as pd
import re


def eval_formula(tags: list, alias: str, formula: str, df: pd.DataFrame) -> pd.DataFrame:
    rename_dict = {"{": "df['", "}": "']"}
    regx_min_max = re.compile(r"(min|max|AVERAGE)\((.+?)\)")
    rep = {'or': 'np.logical_or(', 'and': 'np.logical_and('}
    pattern = "|".join(rep.keys())
    pattern = re.compile(fr"({pattern})\(")
    regx = re.compile(r"\{(.+?)\}")

    df[tags] = df[tags].apply(pd.to_numeric, errors="coerce")  # converting existing tags

    formula = pattern.sub(lambda m: m.group(1).replace(m.group(1), rep[m.group(1)]), formula)
    formula = re.sub(r"(np\.)?(where|isnan|power|exp|logical_or|logical_and|log|abs)\(", r"np.\2(",
                     formula)  # add np. to where
    formula = regx_min_max.sub(
        lambda g: f"df[{regx.findall(g.group(2))}].{g.group(1).replace('AVERAGE', 'mean')}(axis=1)", formula)

    for key, val in rename_dict.items():
        formula = formula.replace(key, val)

    df[alias] = eval(formula)
    return df


def get_calc_cols(df: pd.DataFrame, formula_dict: dict, recur_tag: str = None) -> pd.DataFrame:
    regx = re.compile(r"\{(.*?)\}")
    skipped_tags = []
    print("getting calculated columns")
    formula_dict_copy = formula_dict if recur_tag == None else {recur_tag: formula_dict[recur_tag]}
    # key will be alias, val is formula
    # breakpoint()
    for (alias, formula) in formula_dict_copy.items():
        key = alias
        tags = regx.findall(formula)
        tags = list(set(tags))

        if key in df.columns:
            continue

        elif (set(tags) & set(df.columns)) == set(tags):
            df = eval_formula(tags, alias, formula, df)

        else:
            tags_not_present = []
            for tag in tags:
                if tag in df.columns:
                    pass
                elif tag in formula_dict.keys():
                    df = get_calc_cols(df, formula_dict, tag)

                else:
                    tags_not_present.append(tag)

            if len(tags_not_present) == 0:
                df = eval_formula(tags, alias, formula, df)
            else:
                skipped_tags.append(alias)
    return df


# def run_script():
#     input_data = pd.read_csv(r"D:\AutoML-Outage\input\data.csv")
#     formula_df = pd.read_csv(r"D:\AutoML-Outage\config\features_calc_formula.csv")
#     formula_dict = dict(formula_df[['calc_tag_alias', 'calc_formula']].values)
#
#     input_data.set_index('time', inplace=True)
#     input_data.index = pd.to_datetime(input_data.index)
#
#     result_df = get_calc_cols(input_data, formula_dict)
#     result_df.to_csv(r'D:\AutoML-Outage\output\output_calculated_feature.csv')
#     return result_df
#
#
# run_script()
