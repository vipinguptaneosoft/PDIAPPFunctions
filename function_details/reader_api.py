from fastapi import FastAPI
from typing import List
from datetime import datetime
import pandas as pd
import psycopg2

app = FastAPI()
schema = 'common'

# Database connection settings
DATABASE_HOST = "114.143.58.70"
DATABASE_PORT = 8503
DATABASE_NAME = "IDMS-SWE-DB-QA"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "123456"

# Database connection function
def get_db_conn():
    return psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )


def get_input_data2(tag_list, schema='common', table_name = 'etl_output_data', start_time = '2022-05-01 05:31:00.000', end_time = '2022-05-01 05:41:00.000'):
    print("Input Data")
    print(schema,table_name)
    conn = get_db_conn()
    cur = conn.cursor()


    tag_set = tuple(tag_list)

    query_from_master_tag_list = "select tag, tag_id from common.master_tag_list;"
    cur.execute(query_from_master_tag_list)
    query_from_master_tag_list_response = cur.fetchall()
    # print("QUERY from master_tag_list")
    # print(len(query_from_master_tag_list_response))
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    start_time = datetime.strptime(start_time.strip(), date_format)
    end_time = datetime.strptime(end_time.strip(), date_format)
    query_from_etl_output_data = f"SELECT time_int,value,tag_id FROM {schema}.{table_name} WHERE tag_id IN {tag_set} AND time_int BETWEEN '{int(start_time.timestamp())}' AND '{int(end_time.timestamp())}'"
    cur.execute(query_from_etl_output_data)   
    query_from_etl_output_data_response = cur.fetchall()
    # print(len(query_from_etl_output_data_response))
    # breakpoint()
    cur.close()
    conn.close()


    temp_dataframe = pd.DataFrame(query_from_master_tag_list_response, columns=["tag", "tag_id"] )

    response_dataframe = pd.DataFrame(query_from_etl_output_data_response, columns=["time", "value", "tag_id"] )
    response_dataframe = response_dataframe.merge(temp_dataframe[["tag", "tag_id"]], how="left", on="tag_id")
    response_dataframe.drop_duplicates(subset=["time", "tag"], inplace=True)
    response_dataframe['time'] = pd.to_datetime(response_dataframe['time'], unit='s', utc=True)
    response_dataframe = response_dataframe.pivot(index="time", columns="tag", values="value")
    # breakpoint()
    print(response_dataframe)

    return response_dataframe



# get_data(['292TI1816.PV', '292TI1817A_W.PV', '292TI1837.PV', '292TI1836A_W.PV', '292TI1856A_W.PV'])