## Example from python
from google.cloud import bigquery
import pandas as pd
import numpy as np
import re
import yfinance as yf
import sys
import datetime
import logging
import matplotlib.pyplot as plt
import json
from random import randint

query_id = randint(1, 999999999999)
job_config = bigquery.QueryJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

def tbl_exists(client, table_ref):
    from google.cloud.exceptions import NotFound
    try:
        client.get_table(table_ref)
        return True
    except NotFound:
        return False

def run():
    client = bigquery.Client()
    trunc_query = "DELETE FROM `msds-434-flask-fx-rl-2.fx_reg_bq.curr_data` WHERE query_id != {};".format(str(query_id))
    client.query(trunc_query, job_config=job_config)

    curr = yf.Ticker("EURUSD=X")
    # This will be a configurable call in custom function
    data = curr.history(period="1y", interval="1h")
    data.reset_index(inplace=True)
    data.drop(columns=["Volume", "Dividends", "Stock Splits", "Date"], inplace=True)
    data['query_id'] = query_id

    print(data.columns)

    idx_tr = np.random.choice(np.arange(data.shape[0]), (np.round(data.shape[0]*0.75).astype(int)), False)
    idx_te = set(np.arange(data.shape[0])) - set(idx_tr)
    data["validation"] = "train"
    data.loc[list(idx_te), "validation"] = "test"

    schema = [
        bigquery.SchemaField("Open", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("High", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("Low", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("Close", "FLOAT64", mode="REQUIRED")
    ]

    table = bigquery.Table('msds-434-flask-fx-rl-2.fx_reg_bq.curr_data', schema=schema)

    # if tbl_exists(client, table) is False:
    #     client.create_table(table)  # Make an API request.

    rows_to_insert = data.values.tolist()
    errors = client.insert_rows(table, rows_to_insert)
    print(errors)

    ## Train the model
    # query_model = '''
    # CREATE OR REPLACE MODEL `msds-434-flask-fx-rl-2.fx_reg_bq.regression_model`
    # OPTIONS
    # ( model_type='LOGISTIC_REG',
    #     auto_class_weights=TRUE,
    #     input_label_cols=['Close']
    # ) AS
    # SELECT * EXCEPT (validation) FROM `msds-434-flask-fx-rl-2.fx_reg_bq.curr_data` WHERE validation = 'train'
    # '''
    # model_job = client.query(query_model)
    # print(model_job)

    ## Test set
    query_pred = '''
    SELECT * FROM 
    ML.PREDICT(MODEL `msds-434-flask-fx-rl-2.fx_reg_bq.regression_model`, 
    (SELECT * EXCEPT (validation, query_id) FROM `msds-434-flask-fx-rl-2.fx_reg_bq.curr_data` WHERE validation = 'test' and query_id = {} ) )
    '''.format(query_id)
    
    pred_job = client.query(query_pred)

    out_df = pred_job.result().to_dataframe()

    return out_df

if __name__ == "__main__":
    df = run()
    print(df[-1])
