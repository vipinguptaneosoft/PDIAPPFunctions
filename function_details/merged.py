import pandas as pd


def merge_dataframes(df1, df2, merge_column):
    print("MERGE DATAFRAME")
    print(df1)
    print(df2)
    # breakpoint()
    # Merge the dataframes based on the merge column
    merged_df = pd.merge(df1, df2, on=merge_column, how='outer')
    print('OUTPUT')
    print(merged_df)

    return merged_df


# merged_df = merge_dataframes(df1, df2, 'timestamp')
# print(merged_df)
