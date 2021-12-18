import pandas as pd
import numpy as np
import yfinance as yf
import requests
from copy import deepcopy

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt


class AIModelsApp:

    def home(self, st):

        @st.cache(allow_output_mutation=True)
        def load_df(ativo, start_date, end_date):
            return None

        @ st.cache(allow_output_mutation=True)
        def load_data(option, from_year, to_year):
            if from_year == '' or to_year == '':
                return yf.download(option)
            return yf.download(option, start=f'{from_year}-01-01', end=f'{to_year}-01-01')

        @ st.cache(allow_output_mutation=True)
        def load_csv(name):
            return pd.read_csv(name)

        assets = st.sidebar.multiselect(
            'Qual ativo? ', ('VALE3', 'PETR4', 'ITUB4', 'BIDI11', 'ABEV3'))

        if assets:
            models = st.sidebar.multiselect('Qual modelo?', ('SVR', ))
            st.sidebar.header('Informações para simulação')
            st.sidebar.warning('Clique em simulação para retreinar o modelo')

            from_year = st.sidebar.number_input('Data Inicial', format='%d', value=2019, min_value=2000, max_value=2022, step=1)
            to_year = st.sidebar.number_input('Data Final', format='%d', value=2020, min_value=2000, max_value=2022, step=1)

            if from_year > to_year:
                st.sidebar.error("Data Inicial maior que a Final")
            else:
                if from_year and to_year:
                    deploy = st.sidebar.checkbox('Simulação?')

                    if deploy:
                        train_size_value = st.sidebar.number_input('Treino %', value=80, min_value=0, max_value=90, step=10)

                        test_size_value = st.sidebar.number_input('Teste %', value=int(90 - train_size_value), min_value=0, max_value=int(90 - train_size_value), step=10)

                        deploy_size = st.sidebar.number_input('Simulação %', value=int(100 - (train_size_value + test_size_value)), min_value=int(100 - (train_size_value + test_size_value)), max_value=int(100 - (train_size_value + test_size_value)), step=10)

                        simular = st.sidebar.button(label='Simular')
                    else:
                        train_size_value = st.sidebar.number_input('Treino %', value=80, min_value=0, max_value=90, step=10)
                        test_size_value = st.sidebar.number_input('Teste %', value=int(100 - (train_size_value)), min_value=int(100 - train_size_value), max_value=int(100 - train_size_value), step=10)

                for ativo in assets:
                    if '-' not in ativo:
                        data = load_data(
                            ativo + '.SA', str(int(from_year)), str(int(to_year)))
                    else:
                        data = load_data(ativo, str(
                            int(from_year)), str(int(to_year)))

                    if not models or not from_year or not to_year:
                        st.subheader(f'Gráfico de Preço da {ativo}')
                        st.line_chart(data['Close'])
                    else:
                        for model in models:
                            r_summary = requests.get('https://btk-ai-app.herokuapp.com/setups/svr_model/', json={'name': ativo})

                            model_summary = r_summary.json()['summary']

                            df = load_data(ativo + '.SA', str(int(from_year)), str(int(to_year)))

                            df['Date'] = df.index

                            df['Date'] = pd.to_datetime(df['Date'])
                            df.set_index('Date', drop=False, inplace=True)

                            df = df[str(int(from_year)):str(int(to_year))]

                            df['log_return'] = np.log(df['Close']/df['Close'].shift(-1))

                            df['diff'] = df['High'] - df['Low']

                            df['ma_2'] = df['diff'].rolling(window=2).mean()
                            df['ma_5'] = df['diff'].rolling(window=5).mean()
                            df['ma_10'] = df['diff'].rolling(window=10).mean()
                            df['ma_15'] = df['diff'].rolling(window=15).mean()
                            df['ma_30'] = df['diff'].rolling(window=30).mean()

                            df.loc[df['ma_2'] > df['ma_2'].shift(1), 'tend_2'] = 1
                            df.loc[df['ma_2'] < df['ma_2'].shift(1), 'tend_2'] = -1
                            df.loc[df['ma_2'] == df['ma_2'].shift(1), 'tend_2'] = 0

                            df.loc[df['ma_5'] > df['ma_5'].shift(4), 'tend_5'] = 1
                            df.loc[df['ma_5'] < df['ma_5'].shift(4), 'tend_5'] = -1
                            df.loc[df['ma_5'] == df['ma_5'].shift(4), 'tend_5'] = 0

                            df.loc[df['ma_10'] > df['ma_10'].shift(9), 'tend_10'] = 1
                            df.loc[df['ma_10'] < df['ma_10'].shift(9), 'tend_10'] = -1
                            df.loc[df['ma_10'] == df['ma_10'].shift(9), 'tend_10'] = 0

                            df.loc[df['ma_15'] > df['ma_15'].shift(14), 'tend_15'] = 1
                            df.loc[df['ma_15'] < df['ma_15'].shift(14), 'tend_15'] = -1
                            df.loc[df['ma_15'] == df['ma_15'].shift(14), 'tend_15'] = 0

                            df.loc[df['ma_30'] > df['ma_30'].shift(29), 'tend_30'] = 1
                            df.loc[df['ma_30'] < df['ma_30'].shift(29), 'tend_30'] = -1
                            df.loc[df['ma_30'] == df['ma_30'].shift(29), 'tend_30'] = 0

                            df['desv_2'] = df['log_return'].rolling(window=2).std()
                            df['desv_5'] = df['log_return'].rolling(window=5).std()
                            df['desv_10'] = df['log_return'].rolling(window=10).std()
                            df['desv_15'] = df['log_return'].rolling(window=15).std()
                            df['desv_30'] = df['log_return'].rolling(window=30).std()

                            df.loc[(df['Close'] > df['Close'].shift(2)) & df['desv_2'].notnull(), 'var_2'] = df['desv_2']
                            df.loc[(df['Close'] < df['Close'].shift(2)), 'var_2'] = -df['desv_2']

                            df.loc[(df['Close'] > df['Close'].shift(5)) & df['desv_5'].notnull(), 'var_5'] = df['desv_5']
                            df.loc[(df['Close'] < df['Close'].shift(5)), 'var_5'] = -df['desv_5']

                            df.loc[(df['Close'] > df['Close'].shift(10)) & df['desv_10'].notnull(), 'var_10'] = df['desv_10']
                            df.loc[(df['Close'] < df['Close'].shift(10)), 'var_10'] = -df['desv_10']

                            df.loc[(df['Close'] > df['Close'].shift(15)) & df['desv_15'].notnull(), 'var_15'] = df['desv_15']
                            df.loc[(df['Close'] < df['Close'].shift(15)), 'var_15'] = -df['desv_15']

                            df.loc[(df['Close'] > df['Close'].shift(30)) & df['desv_30'].notnull(), 'var_30'] = df['desv_30']
                            df.loc[(df['Close'] < df['Close'].shift(30)), 'var_30'] = -df['desv_30']

                            df['ma_2'].fillna(df['ma_2'].mean(), inplace=True)
                            df['ma_5'].fillna(df['ma_5'].mean(), inplace=True)
                            df['ma_10'].fillna(df['ma_10'].mean(), inplace=True)
                            df['ma_15'].fillna(df['ma_15'].mean(), inplace=True)
                            df['ma_30'].fillna(df['ma_30'].mean(), inplace=True)

                            df['tend_2'].fillna(0, inplace=True)
                            df['tend_5'].fillna(0, inplace=True)
                            df['tend_10'].fillna(0, inplace=True)
                            df['tend_15'].fillna(0, inplace=True)
                            df['tend_30'].fillna(0, inplace=True)

                            df['desv_2'].fillna(df['desv_2'].median(), inplace=True)
                            df['var_2'].fillna(df['var_2'].median(), inplace=True)

                            df['desv_5'].fillna(df['desv_5'].median(), inplace=True)
                            df['var_5'].fillna(df['var_5'].median(), inplace=True)

                            df['desv_10'].fillna(df['desv_10'].median(), inplace=True)
                            df['var_10'].fillna(df['var_10'].median(), inplace=True)

                            df['desv_15'].fillna(df['desv_15'].median(), inplace=True)
                            df['var_15'].fillna(df['var_15'].median(), inplace=True)

                            df['desv_30'].fillna(df['desv_30'].median(), inplace=True)
                            df['var_30'].fillna(df['var_30'].median(), inplace=True)

                            data_ativo = deepcopy(df)

                            df.drop(['Volume', 'Adj Close', 'log_return', 'tend_2', 'tend_5', 'tend_10', 'tend_15', 'tend_30', 'Date'], axis=1, inplace=True)

                            list_to_pred = df.iloc[-1].tolist()

                            y_pred = requests.get('https://btk-ai-app.herokuapp.com/setups/svr_model/predict', json={'name': ativo, 'data': list_to_pred})

                            st.subheader(f'{ativo} - Modelo {model} de {int(from_year)} até {int(to_year)}')

                            if deploy:
                                train_value = int(len(data_ativo)*((1-deploy_size/100) - train_size_value/100))
                                test_value = int(len(data_ativo)*((1-deploy_size/100) - test_size_value/100))
                                deploy_value = int(len(data_ativo)*((train_size_value/100 + test_size_value/100)) - deploy_size/100)

                                __treino = go.Scatter(
                                    x=data_ativo['Date'].iloc[:test_value],
                                    y=data_ativo['Close'].iloc[:test_value],
                                    # fill='tonexty', # fill area between trace0 and trace1
                                    mode='lines', line_color='#03adfc',
                                    name='Treino'
                                )

                                __teste = go.Scatter(
                                    x=data_ativo['Date'].iloc[test_value -
                                                              1:deploy_value],
                                    y=data_ativo['Close'].iloc[test_value -
                                                               1:deploy_value],
                                    # fill='tozeroy', # fill area between trace0 and trace1
                                    mode='lines', line_color='#ce03fc', name='Teste'
                                )

                                __simulacao = go.Scatter(
                                    x=data_ativo['Date'].iloc[deploy_value-1:],
                                    y=data_ativo['Close'].iloc[deploy_value-1:],
                                    # fill='tozeroy', # fill area between trace0 and trace1
                                    mode='lines', line_color='#03fc90',
                                    name='Simulação'
                                )

                                scatter_data = [__treino, __teste, __simulacao]
                                group_labels = ['Treino', 'Teste', 'Simulação']

                                layout = go.Layout(legend=dict(traceorder="reversed"), xaxis=dict(
                                    showgrid=False), yaxis=dict(showgrid=False))

                            else:
                                train_value = int(len(data_ativo)*(1 - train_size_value/100))
                                test_value = int(len(data_ativo)*(1 - test_size_value/100))
                                deploy_value = len(data_ativo)

                                __treino = go.Scatter(
                                    x=data_ativo['Date'].iloc[:test_value],
                                    y=data_ativo['Close'].iloc[:test_value],
                                    # fill='tonexty',  # fill area between trace0 and trace1
                                    mode='lines', line_color='#03adfc',
                                    name='Treino'
                                )

                                __teste = go.Scatter(
                                    x=data_ativo['Date'].iloc[test_value-1:],
                                    y=data_ativo['Close'].iloc[test_value-1:],
                                    # fill='tozeroy', # fill area between trace0 and trace1
                                    mode='lines', line_color='#ce03fc', name='Teste'
                                )

                                scatter_data = [__treino, __teste]
                                group_labels = ['Treino', 'Teste']

                                layout = go.Layout(legend=dict(traceorder="reversed"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

                            fig = go.Figure()
                            fig.update_xaxes(gridwidth=1, gridcolor='#444')
                            fig.update_yaxes(gridwidth=1, gridcolor='#444')

                            fig.add_trace(__treino)
                            fig.add_trace(__teste)

                            if deploy:
                                fig.add_trace(__simulacao)

                            st.plotly_chart(fig, use_container_width=True)

                            if y_pred.json()['prediction'] > data_ativo['log_return'].iloc[-1]:
                                st.success("COMPRA")
                            else:
                                st.error("VENDA")

                            if deploy:
                                with fig.batch_update():
                                    fig.add_trace(__simulacao)

                                json = {
                                    'name': ativo,
                                    'start_date': f'{str(int(from_year))}-01-01',
                                    'end_date': f'{str(int(to_year))}-01-01',
                                    'train_size': train_size_value/100,
                                    'test_size': test_size_value/100,
                                    'deploy_size': deploy_size/100
                                }

                                if simular:
                                    response = requests.get(f'https://btk-ai-app.herokuapp.com/setups/{model.lower()}_model/fit', json=json)

                                    if response.status_code == 200:
                                        r_summary = requests.get(f'https://btk-ai-app.herokuapp.com/setups/{model.lower()}_model/', json={'name': ativo})
                                        model_summary = r_summary.json()['summary']
                            else:
                                json = {
                                    'name': ativo,
                                    'start_date': f'{str(int(from_year))}-01-01',
                                    'end_date': f'{str(int(to_year))}-01-01',
                                    'train_size': train_size_value/100,
                                    'test_size': test_size_value/100,
                                    'deploy_size': 0.0
                                }

                                response = requests.get(f'https://btk-ai-app.herokuapp.com/setups/{model.lower()}_model/fit', json=json)

                                if response.status_code == 200:
                                    r_summary = requests.get(f'https://btk-ai-app.herokuapp.com/setups/{model.lower()}_model/', json={'name': ativo})
                                    model_summary = r_summary.json()['summary']

                            with st.expander('Mais detalhes'):
                                st.subheader('Métricas (% de erro)')

                                for col, key in zip(st.columns(len(model_summary)), model_summary):
                                    with col:
                                        st.write(
                                            f'{key}: ', model_summary[key], ' %')

                                st.subheader('Histórico do modelo')
                                st.write(data.tail(10))
                                st.subheader('Relatório do modelo')
                                st.download_button('Documento', data=f'static/docs/{ativo}/{model}.pdf', file_name=f'{ativo}_{model}_BTK.pdf')
