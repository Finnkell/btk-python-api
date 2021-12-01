# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:54:51 2021

@author: OPR11
"""

import pandas as pd
from minio import Minio
from io import BytesIO
import urllib3
import requests
from io import StringIO

# df = pd.read_csv('D:/seq/SEQL3_BOV_T.csv', parse_dates=[['<date>', '<time>']])
access_key = 'JGBBW2AVEAIVA9IMOWF2'
secret_key = 'GE6bKVVrRj19MJ1TjdERxaGAoMXVBNZdgY8GMPf7'
client = Minio("host.docker.internal:9000", access_key=access_key, secret_key=secret_key, secure=False)
# %%
data = pd.read_csv(client.get_object('landing', 'SEQL3_BOV_T.csv'))[['<date>', '<time>', '<price>', '<qty>']].to_csv(index=False).encode('utf8')
found = client.bucket_exists("process")
if not found:
    client.make_bucket("process")
client.put_object("process", "SEQL3_BOV_T.csv", BytesIO(data), length=len(data), content_type="application/csv_binary")
# %%
a = client.get_object('process', 'SEQL3_BOV_T.csv',)
a = pd.read_csv(a)
print(a.head())
# %%
for b in client.list_objects('landing'):
    print(b.object_name)
c = b.object_name
# r = requests.get(a, stream=True)
# %%
df = pd.read_csv(client.get_object('landing', 'SEQL3_BOV_T.csv'), parse_dates=[['<date>', '<time>']])[['<date>_<time>', '<price>', '<qty>']]
gp = df.groupby(df['<date>_<time>'].dt.floor('1T'))
# del df
df2 = gp['<price>'].agg('ohlc')
df2['volume'] = gp['<qty>'].agg(sum)
df2['tick'] = gp['<price>'].agg('count')
df2.reset_index(inplace=True)
df2.rename(columns={'<date>_<time>': 'date_time'}, inplace=True)
# del gp
