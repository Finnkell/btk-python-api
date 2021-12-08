import pandas as pd
import numpy as np
import yfinance as yf
import requests

import plotly.express as px
import plotly.graph_objects as go

from pages.markowitz.Markowits import markowitz


class MarkowitzApp:

    def home(self, st):

        @st.cache
        def convert_csv(data):
            return data.to_csv(index=False).encode('utf-8')

        @st.cache
        def load_data(option):
            return yf.download(option)

        @st.cache
        def load_json():
            return pd.read_json('static/stocks.json')

        # stocks = load_json()
        # tickets = (stocks['stocks'])

        window_option = st.sidebar.selectbox(
            'Método', ('Markowitz para ações', 'Markowitz para modelos de IA', ))

        if window_option == 'Markowitz para ações':
            st.header('Método de Markowitz para ações')

            symbols = ["JPM", "NFLX","AAPL" , "LOW" , "QRVO" , "AES" , "BEN" , "LRCX"  , "NUE" ,  "EXPD"]

            assets = st.sidebar.multiselect('Selecione sua carteira de ativos', symbols)

            if len(assets) >= 2:
                from_year = st.sidebar.number_input('Data Inicial', format='%d', value=2019, min_value=2000, max_value=2022, step=1)
                to_year = st.sidebar.number_input('Data Final', format='%d', value=2020, min_value=2000, max_value=2022, step=1)
                
                if from_year > to_year:
                    st.sidebar.error("Data Inicial maior que a Final")
                else:
                    ok = st.sidebar.button('Aplicar Markowitz')
                
                    if ok:
                        df_symbols = yf.download(assets, start=f'{from_year}-01-01', end=f'{to_year}-12-31', progress=False)['Close']
                        
                        markowitz(df_symbols, st)