import pandas as pd
import numpy as np
import yfinance as yf
import requests

import plotly.express as px
import plotly.graph_objects as go


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

        stocks = load_json()
        tickets = (stocks['stocks'])

        window_option = st.sidebar.selectbox(
            'Método', ('Markowitz para ações', 'Markowitz para modelos de IA', ))

        if window_option == 'Markowitz para ações':
            st.header('Método de Markowitz para ações')

            qtd_ativos = st.sidebar.text_input('Quantidade de ativos')

            if qtd_ativos != '':
                for i in range(int(qtd_ativos)):
                    st.sidebar.selectbox(f'Ativo {i}', tickets)
            st.write(MarkowitzStocks())
