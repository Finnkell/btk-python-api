import streamlit as st
import requests
import json


BODY = {
    "name": "BIDI11",
    "data": [
            12435,
            1234,
            1234,
            1234,
            1234,
            123412,
            123415,
            12435,
            1234,
            1234,
            1234,
            1234,
            123412,
            123415,
            12435,
            1234,
            1234,
            1234,
            1234,
            123412
    ]
}

st.header('Teste')

response = requests.get(
    'http://127.0.0.1:8000/setups/svr_model/predict', json=BODY)

st.write(response.json()['prediction']*100)
