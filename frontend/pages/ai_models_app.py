import pandas as pd
import numpy as np
import yfinance as yf
import requests

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt


class AIModelsApp:

    def home(self, st):

        @st.cache(allow_output_mutation=True)
        def load_data(option, from_year, to_year):
            if from_year == '' or to_year == '':
                return yf.download(option)
            return yf.download(option, start=f'{from_year}-01-01', end=f'{to_year}-01-01')

        @st.cache(allow_output_mutation=True)
        def load_csv(name):
            return pd.read_csv(name)

        assets = st.sidebar.multiselect(
            'Qual ativo? ', ('VALE3', 'PETR4', 'ITUB4', 'BIDI11', 'ABEV3'))

        if assets:
            models = st.sidebar.multiselect('Qual modelo?', ('SVR', ))
            st.sidebar.header('Informações para simulação')
            st.sidebar.warning('Clique em simulação para retreinar o modelo')

            from_year = st.sidebar.number_input(
                'Data Inicial', format='%d', value=2019, min_value=2000, max_value=2022, step=1)
            to_year = st.sidebar.number_input(
                'Data Final', format='%d', value=2020, min_value=2000, max_value=2022, step=1)

            if from_year > to_year:
                st.sidebar.error("Data Inicial maior que a Final")
            else:
                if from_year and to_year:
                    deploy = st.sidebar.checkbox('Simulação?')

                    if deploy:
                        train_size_value = st.sidebar.number_input(
                            'Treino %', value=80, min_value=0, max_value=90, step=10)

                        test_size_value = st.sidebar.number_input('Teste %', value=int(
                            90 - train_size_value), min_value=0, max_value=int(90 - train_size_value), step=10)

                        deploy_size = st.sidebar.number_input('Simulação %', value=int(100 - (train_size_value + test_size_value)), min_value=int(
                            100 - (train_size_value + test_size_value)), max_value=int(100 - (train_size_value + test_size_value)), step=10)

                        simular = st.sidebar.button(label='Simular')
                    else:
                        train_size_value = st.sidebar.number_input(
                            'Treino %', value=80, min_value=0, max_value=90, step=10)
                        test_size_value = st.sidebar.number_input('Teste %', value=int(
                            100 - (train_size_value)), min_value=int(100 - train_size_value), max_value=int(100 - train_size_value), step=10)

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
                            r_summary = requests.get(
                                'https://btk-ai-app.herokuapp.com/setups/svr_model/', json={'name': ativo})

                            model_summary = r_summary.json()['summary']

                            data_ativo = load_data(
                                ativo + '.SA', str(int(from_year)), str(int(to_year)))

                            data_ativo['Date'] = data_ativo.index

                            data_ativo['log_return'] = np.log(
                                data_ativo['Close']/data_ativo['Close'].shift(1)).fillna(data_ativo['Close'].mean())

                            st.subheader(
                                f'{ativo} - Modelo {model} de {int(from_year)} até {int(to_year)}')

                            if deploy:
                                train_value = int(
                                    len(data_ativo)*((1-deploy_size/100) - train_size_value/100))
                                test_value = int(
                                    len(data_ativo)*((1-deploy_size/100) - test_size_value/100))
                                deploy_value = int(
                                    len(data_ativo)*((train_size_value/100 + test_size_value/100)) - deploy_size/100)

                                __treino = go.Scatter(
                                    x=data_ativo['Date'].iloc[:test_value],
                                    y=data_ativo['Close'].iloc[:test_value],
                                    # fill='tonexty', # fill area between trace0 and trace1
                                    mode='lines', line_color='#03adfc',
                                    name='Treino'
                                )

                                __teste = go.Scatter(
                                    x=data_ativo['Date'].iloc[test_value:deploy_value],
                                    y=data_ativo['Close'].iloc[test_value:deploy_value],
                                    # fill='tozeroy', # fill area between trace0 and trace1
                                    mode='lines', line_color='#ce03fc', name='Teste'
                                )

                                __simulacao = go.Scatter(
                                    x=data_ativo['Date'].iloc[deploy_value:],
                                    y=data_ativo['Close'].iloc[deploy_value:],
                                    # fill='tozeroy', # fill area between trace0 and trace1
                                    mode='lines', line_color='#03fc90',
                                    name='Simulação'
                                )

                                scatter_data = [__treino, __teste, __simulacao]
                                group_labels = ['Treino', 'Teste', 'Simulação']

                                layout = go.Layout(legend=dict(traceorder="reversed"), xaxis=dict(
                                    showgrid=False), yaxis=dict(showgrid=False))

                            else:
                                train_value = int(
                                    len(data_ativo)*(1 - train_size_value/100))
                                test_value = int(
                                    len(data_ativo)*(1 - test_size_value/100))
                                deploy_value = len(data_ativo)

                                __treino = go.Scatter(
                                    x=data_ativo['Date'].iloc[:test_value],
                                    y=data_ativo['Close'].iloc[:test_value],
                                    # fill='tonexty', # fill area between trace0 and trace1
                                    mode='lines', line_color='#03adfc',
                                    name='Treino'
                                )

                                __teste = go.Scatter(
                                    x=data_ativo['Date'].iloc[test_value:],
                                    y=data_ativo['Close'].iloc[test_value:],
                                    # fill='tozeroy', # fill area between trace0 and trace1
                                    mode='lines', line_color='#ce03fc', name='Teste'
                                )

                                scatter_data = [__treino, __teste]
                                group_labels = ['Treino', 'Teste']

                                layout = go.Layout(legend=dict(traceorder="reversed"), xaxis=dict(
                                    showgrid=False), yaxis=dict(showgrid=False))

                            fig = go.Figure()

                            fig.add_trace(__treino)
                            fig.add_trace(__teste)

                            if deploy:
                                fig.add_trace(__simulacao)

                            st.plotly_chart(fig, use_container_width=True)

                            y_pred = requests.get('https://btk-ai-app.herokuapp.com/setups/svr_model/predict', json={
                                'name': ativo, 'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]})

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
                                    response = requests.get(
                                        f'https://btk-ai-app.herokuapp.com/setups/{model.lower()}_model/fit', json=json)

                                    if response.status_code == 200:
                                        r_summary = requests.get(
                                            'https://btk-ai-app.herokuapp.com/setups/svr_model/', json={'name': ativo})
                                        model_summary = r_summary.json()[
                                            'summary']
                            else:
                                json = {
                                    'name': ativo,
                                    'start_date': f'{str(int(from_year))}-01-01',
                                    'end_date': f'{str(int(to_year))}-01-01',
                                    'train_size': train_size_value/100,
                                    'test_size': test_size_value/100,
                                    'deploy_size': 0.0
                                }

                                response = requests.get(
                                    f'https://btk-ai-app.herokuapp.com/setups/{model.lower()}_model/fit', json=json)

                                if response.status_code == 200:
                                    r_summary = requests.get(
                                        'https://btk-ai-app.herokuapp.com/setups/svr_model/', json={'name': ativo})
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
                                st.download_button(
                                    'Documento', data=f'static/docs/{ativo}/{model}.pdf', file_name=f'{ativo}_{model}_BTK.pdf')
