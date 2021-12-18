import pandas as pd
import numpy as np
import yfinance as yf
import requests

import plotly.express as px
import plotly.graph_objects as go

from pages.markowitz_plot.markowits_plot import plot_normalized_price, plot_annualized_returns, plot_annualized_volatility, plot_monte_carlo_simulated_allocation, plot_int

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
                # TODO: O USUÁRIO COLOCAR A PORCENTAGEM DE CAPITAL PARA CADA ATIVO
                
                # st.sidebar.markdown('Deseja colocar porcentagem dividida para cada ativo?')
                # weight_button = st.sidebar.button('Sim')

                # if weight_button:
                #     st.write('-------')
                #     wallet_weights = []
                #     max_weight = 100.0

                #     for asset in assets:
                #         porcentagem = st.sidebar.number_input(f'Porcentagem aplicada em {asset}', format='%f', value=1.0, min_value=1.0, max_value=float(max_weight), step=1.0)
                #         max_weight = int(max_weight - porcentagem)
                        
                #         # train_size_value = st.sidebar.number_input('Treino %', value=80, min_value=0, max_value=90, step=10)
                #         # test_size_value = st.sidebar.number_input('Teste %', value=int(90 - train_size_value), min_value=0, max_value=int(90 - train_size_value), step=10)
                #         # deploy_size = st.sidebar.number_input('Simulação %', value=int(100 - (train_size_value + test_size_value)), min_value=int(100 - (train_size_value + test_size_value)), max_value=int(100 - (train_size_value + test_size_value)), step=10)
                        
                #         print(f'max_weight: {max_weight}')

                #         wallet_weights.append(porcentagem)

                #     st.sidebar.write(wallet_weights)
                #     st.sidebar.write('-------')

                from_year = st.sidebar.number_input('Data Inicial', format='%d', value=2019, min_value=2000, max_value=2022, step=1)
                to_year = st.sidebar.number_input('Data Final', format='%d', value=2020, min_value=2000, max_value=2022, step=1)

                if from_year > to_year:
                    st.sidebar.error('Data Inicial maior que a Final')
                else:
                    ok = st.sidebar.button('Aplicar Markowitz')

                    if ok:
                        json_data = {
                            'start_date': from_year,
                            'end_date': to_year,
                            'assets': assets
                        }
                        
                        response_data = requests.get('http://localhost:8000/tools/markowitz/', json=json_data)
                        
                        try:
                            df_data = response_data.json()['assets_data']
                            try:
                                fig = plot_normalized_price(df_data)
                                st.pyplot(fig)
                            except:
                                st.error('Erro ao mostrar o gráfico de dados normalizados')    
                        except:
                            st.error('Erro ao receber os dados normalizados')
                            
                        
                        
                        # print(f'from_year: {from_year} | to_year: {to_year}')
                        # df_symbols = yf.download(assets, start=f'{str(from_year)}-01-01', end=f'{str(to_year)}-12-31', progress=False)['Close']
                        
                        # df_symbols.dropna(axis=0, inplace=True)
                        
                        # markowitz(df_symbols, st)