# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:10:36 2021

@author: OPR11
"""

# [START tutorial]
# [START import_module]
from datetime import datetime
# The DAG object; we'll need this to instantiate a DAG
from minio import Minio
from io import BytesIO
# Operators; we need this to operate!
from airflow.decorators import dag, task
# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
}
# [END default_args]
@dag(schedule_interval='30 2 * * *', start_date=datetime(2021, 1, 1), catchup=False, tags=['ohlc'])
def new_ohlc():

    @task()
    def get_csv(name, bucket, process_bucket):
        import pandas as pd
        try:
            response = client.get_object(bucket, name,)
            data = pd.read_csv(response)[['<date>', '<time>', '<price>', '<qty>']].to_csv(index=False).encode('utf8')
        finally:
            response.close()
            response.release_conn()
        found = client.bucket_exists(process_bucket)
        if not found:
            client.make_bucket(process_bucket)
        result = client.put_object(process_bucket, name, BytesIO(data), length=len(data), content_type="application/csv")
        return name

    @task()    
    def process_csv(name, bucket, timeframe):
        import pandas as pd
        try:
            response = client.get_object(bucket, name,)
            data = pd.read_csv(response, parse_dates=[['<date>', '<time>']])
        finally:
            response.close()
            response.release_conn()
        gp = data.groupby(data['<date>_<time>'].dt.floor(timeframe))
        del data
        df = gp['<price>'].agg('ohlc')
        df['volume'] = gp['<qty>'].agg(sum)
        df['tick'] = gp['<price>'].agg('count')
        del gp
        df.reset_index(inplace=True)
        df.rename(columns={'<date>_<time>': 'date_time'}, inplace=True)
        data = df.to_csv(index=False).encode('utf8')
        filename = "OHLC_" + timeframe + "_"+ name
        result = client.put_object(bucket, filename, BytesIO(data), length=len(data), content_type="application/csv")        
        return filename

    @task()
    def send_csv(name, process_bucket, curated_bucket, timeframe):
        import pandas as pd
        try:
            response = client.get_object(process_bucket, name,)
            data = pd.read_csv(response).to_csv(index=False).encode('utf8')
        finally:
            response.close()
            response.release_conn()
        result = client.put_object(curated_bucket, name, BytesIO(data), length=len(data), content_type="application/csv") 

    timeframes = ['1S', '10S', '30S', '1Min', '5Min', '10Min', '15Min', '30Min', '1H', '4H', '12H', '1D']
    # timeframes = ['W']
    access_key = 'JGBBW2AVEAIVA9IMOWF2'
    secret_key = 'GE6bKVVrRj19MJ1TjdERxaGAoMXVBNZdgY8GMPf7'
    client = Minio("host.docker.internal:9000", access_key=access_key, secret_key=secret_key, secure=False)
    for file in client.list_objects('landing'):
        name = file.object_name
        if not name.startswith(('OHLC_', 'NEW_OHLC', 'R_OHLC', 'VWAP_', 'tapereading_')) and name.endswith((".csv", ".CSV")):
            name = get_csv(name, file._bucket_name, 'process')
            for timeframe in timeframes:
                filename = process_csv(name, 'process', timeframe)
                send_csv(filename, 'process', 'curated', timeframe)


# [END main_flow]
etl_NEW_ohlc_dag = new_ohlc()
# [END tutorial]