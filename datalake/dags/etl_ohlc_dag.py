# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:33:58 2021

@author: OPR11
"""
import numpy as np
import pandas as pd
import os
import sys
from datetime import datetime
from minio import Minio
from io import BytesIO

from airflow.decorators import dag, task


@dag(schedule_interval=None, start_date=datetime(2021, 1, 1), catchup=False, tags=['example'])
def ohlc_dag():
    

    @task()
    def ohlc():
        def first(array):
            return array[0]

        def last(array):
            return array[-1]


        def vfl(array):
            return int(np.argmax(array) < np.argmin(array))  # high antes que o low


        def round_price_row_ind(row):
            # print(row)
            if row['<trade_type>'] == 'AggressorSeller':
                if (row['<price>'] * 10) % 10 > 5:
                    return ((row['<price>'] // 10) * 10) + 5
                else:
                    return ((row['<price>'] // 10) * 10)
            else:
                if (row['<price>'] * 10) % 10 > 5:
                    return ((row['<price>'] // 10) * 10) + 10
                else:
                    return ((row['<price>'] // 10) * 10) + 5


        def round_price_row_dol(row):
            if row['<trade_type>'] == 'AggressorSeller':
                if row['<price>'] % 10 > 5:
                    return ((((row['<price>'] * 10) // 10) * 10) + 5) / 10
                else:
                    return ((((row['<price>'] * 10) // 10) * 10)) / 10
            else:
                if row['<price>'] % 10 > 5:
                    return ((((row['<price>'] * 10) // 10) * 10) + 10) / 10
                else:
                    return ((((row['<price>'] * 10) // 10) * 10) + 5) / 10


        def round_price_row_bov(row):
            if row['<trade_type>'] == 'AggressorSeller':
                return row['<price>'] - 0.01
            elif row['<trade_type>'] == 'AggressorBuyer':
                return row['<price>'] + 0.01
            else:
                return row['<price>']

        def ohlc(df, freq='1S', price='<price>'):
            gp = df.groupby(df['<date>_<time>'].dt.floor(freq))
            print(price + ' grouped')
            del df
            df2 = gp[price].apply(list)
            df4 = gp['<qty>'].apply(list)
            del gp
            # df2 = df2.apply(lambda y: np.nan if len(y) == 0 else y)
            # df2.dropna(inplace=True)
            # df2['<price>'] = df2.apply(lambda x: np.nan if len(x) == 0 else x).dropna()
            df2 = pd.DataFrame(df2)
            df2 = df2[df2[price].str.len() > 0]
            # debug = df2
            df2['<LOW>'] = df2[price].apply(np.amin)
            df2['<HIGH>'] = df2[price].apply(np.amax)
            df2['<VFL>'] = df2[price].apply(vfl)
            df2['<OPEN>'] = df2[price].apply(first)
            df2['<CLOSE>'] = df2[price].apply(last)
            df2['<VOL>'] = df4.apply(sum)
            del df4
            df2['<date>_<time>2'] = df2.index
            df2 = df2.reset_index()
            df2['<DATE>_<TIME>'] = df2['<date>_<time>2']
            df2 = df2.drop(columns='<date>_<time>2')
            df2['<TICK>'] = df2[price].apply(len)
            df2 = df2.drop(columns=price)
            df2['<date>_<time>'] = pd.to_datetime(df2['<date>_<time>'], errors='coerce')
            # df2 = df2[df2['<date>_<time>'].dt.hour <= 17]
            # df2 = df2[df2['<date>_<time>'].dt.hour >= 10]
            df2 = df2[['<DATE>_<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<TICK>', '<VOL>', '<VFL>']]
            # df2 = df2[['<DATE>_<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<TICK>', '<VOL>']]
            return df2


        access_key = 'JGBBW2AVEAIVA9IMOWF2'
        secret_key = 'GE6bKVVrRj19MJ1TjdERxaGAoMXVBNZdgY8GMPf7'
        client = Minio("host.docker.internal:9000", access_key=access_key, secret_key=secret_key, secure=False)
        chunksize = 100
        chunksize = chunksize * 1000000
        for file in client.list_objects('landing'):
            name = file.object_name
            if not name.startswith(('OHLC_', 'NEW_OHLC', 'R_OHLC', 'VWAP_', 'tapereading_')) and name.endswith((".csv", ".CSV")):
                print(name + ' loaded')
                i = 1
                with pd.read_csv(client.get_object('landing', name), chunksize=chunksize, iterator=True, parse_dates=[['<date>', '<time>']]) as reader:
                    for chunk in reader:
                        # if i > 1: break
                        # chunk['<newprice>'] = chunk['<vol>'] / chunk['<qty>']
                        # if 'BOV' in name:
                        #     print('bov')
                        #     chunk['<rprice>'] = chunk.apply(round_price_row_bov, axis=1)
                        # elif 'DO' in name:
                        #     chunk['<rprice>'] = chunk.apply(round_price_row_dol, axis=1)
                        #     print('dol')
                        # else:
                        #     chunk['<rprice>'] = chunk.apply(round_price_row_ind, axis=1)
                        #     print('ind')
                        if i == 1 and len(chunk.index) < chunksize:
                            df_ohlc = ohlc(chunk)
                            # df_newohlc = ohlc(chunk, price='<newprice>')
                            # df_rohlc = ohlc(chunk, price='<rprice>')
                        elif i == 1:
                            chunk_tail = chunk[chunk['<date>_<time>'].dt.floor('S') == chunk['<date>_<time>'].iloc[-1].floor('S')]
                            df_ohlc = ohlc(chunk[chunk['<date>_<time>'].dt.floor('S') != chunk['<date>_<time>'].iloc[-1].floor('S')])
                            # df_newohlc = ohlc(chunk[chunk['<date>_<time>'].dt.floor('S') != chunk['<date>_<time>'].iloc[-1].floor('S')], price='<newprice>')
                            # df_rohlc = ohlc(chunk[chunk['<date>_<time>'].dt.floor('S') != chunk['<date>_<time>'].iloc[-1].floor('S')], price='<rprice>')

                        elif(len(chunk.index) < chunksize):
                            chunk = pd.concat([chunk_tail, chunk]).reset_index(drop=True)
                            df_ohlc = pd.concat([df_ohlc, ohlc(chunk)]).reset_index(drop=True)
                            # df_newohlc = pd.concat([df_newohlc, ohlc(chunk, price='<newprice>')]).reset_index(drop=True)
                            # df_rohlc = pd.concat([df_rohlc, ohlc(chunk, price='<rprice>')]).reset_index(drop=True)
                        else:
                            chunk = pd.concat([chunk_tail, chunk]).reset_index(drop=True)
                            chunk_tail = chunk[chunk['<date>_<time>'].dt.floor('S') == chunk['<date>_<time>'].iloc[-1].floor('S')]
                            df_ohlc = pd.concat([df_ohlc, ohlc(chunk[chunk['<date>_<time>'].dt.floor('S') != chunk['<date>_<time>'].iloc[-1].floor('S')])]).reset_index(drop=True)
                            # df_newohlc = pd.concat([df_newohlc, ohlc(chunk[chunk['<date>_<time>'].dt.floor('S') != chunk['<date>_<time>'].iloc[-1].floor('S')], price='<newprice>')]).reset_index(drop=True)
                            # df_rohlc = pd.concat([df_rohlc, ohlc(chunk[chunk['<date>_<time>'].dt.floor('S') != chunk['<date>_<time>'].iloc[-1].floor('S')], price='<rprice>')]).reset_index(drop=True)
                        print(i)
                        i += 1
                    # if not os.path.exists(root + '/ohlc/new ohlc'):
                    #     os.makedirs(root + '/ohlc/new ohlc')
                    # if not os.path.exists(root + '/ohlc/rohlc'):
                    #     os.makedirs(root + '/ohlc/rohlc')
                    data = df_ohlc.to_csv(index=False).encode('utf8')
                    client.put_object("process", "OHLC_" + name, BytesIO(data), length=len(data), content_type="application/csv")
                    # df_newohlc.to_csv(root + '/ohlc/new ohlc/NEW_OHLC_1S' + name, index=False)
                    # df_rohlc.to_csv(root + '/ohlc/rohlc/R_OHLC_1S' + name, index=False)
                    print(name + ' to csv')
    

    ohlc()

etl_ohlc_dag = ohlc_dag()