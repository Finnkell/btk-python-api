import pandas as pd
import numpy as np
import yfinance as yf
import requests

import plotly.express as px
import plotly.graph_objects as go


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
            'Qual ativo? ', ('VALE3', 'PETR4', 'ITUB4', 'BIDI11'))

        if assets:
            models = st.sidebar.multiselect('Qual modelo?', ('SVR', ))
            st.sidebar.header('Informações para simulação')
            st.sidebar.warning(
                'Clique em simulação para retreinar o modelo')

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
                        st.subheader(f'{ativo}')
                        st.line_chart(data['Close'])
                    else:
                        for model in models:
                            r_summary = requests.get(
                                'http://127.0.0.1:8000/setups/svr_model/', json={'name': ativo})
                            model_summary = r_summary.json()['summary']

                            data_ativo = load_data(
                                ativo + '.SA', str(int(from_year)), str(int(to_year)))

                            data_ativo['log_return'] = np.log(
                                data_ativo['Close']/data_ativo['Close'].shift(1)).fillna(data_ativo['Close'].mean())

                            y_pred = requests.get('http://127.0.0.1:8000/setups/svr_model/predict', json={
                                'name': ativo, 'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]})

                            st.subheader(
                                f'{ativo} - Modelo {model} de {int(from_year)} até {int(to_year)}')

                            # train_size = len(y_train.index)
                            # test_size = len(y_test.index)
                            # # pred_size = len(pd.DataFrame(y_pred).index)

                            # concat = pd.concat([y_train, y_test], ignore_index=True)

                            # plt_train = concat.copy()
                            # plt_test = concat.copy()
                            # # plt_pred = concat.copy()

                            # plt_train.iloc[:train_size] = None
                            # plt_test.iloc[train_size:] = None
                            # # plt_pred.iloc[:train_size] = None

                            # df = pd.DataFrame()

                            # df['Test'] = plt_train
                            # df['Train'] = plt_test
                            # # df['Pred'] = plt_pred

                            # fig_pyplot, ax = plt.subplots(figsize=(15, 15))
                            # ax.plot(df['Test'])
                            # ax.plot(df['Train'])

                            # fig = px.line(df)
                            # fig.update_layout(template='plotly_dark')

                            # st.pyplot(fig_pyplot)
                            st.line_chart(data_ativo['Close'])
                            # st.plotly_chart(fig)

                            if y_pred.json()['prediction'] > data_ativo['log_return'].iloc[-2]:
                                st.success("COMPRA")
                            else:
                                st.error("VENDA")

                            if deploy:
                                if st.sidebar.button('Simular'):
                                    json = {
                                        'name': ativo,
                                        'start_date': f'{str(int(from_year))}-01-01',
                                        'end_date': f'{str(int(to_year))}-01-01',
                                        'train_size': train_size_value/100,
                                        'test_size': test_size_value/100,
                                        'deploy_size': deploy_size/100
                                    }
                                    response = requests.get(
                                        f'http://127.0.0.1:8000/setups/{model.lower()}_model/fit', json=json)

                                    if response.status_code == 200:
                                        r_summary = requests.get(
                                            'http://127.0.0.1:8000/setups/svr_model/', json={'name': ativo})
                                        model_summary = r_summary.json()[
                                            'summary']

                            else:
                                if st.sidebar.button('Simular'):
                                    json = {
                                        'name': ativo,
                                        'start_date': f'{str(int(from_year))}-01-01',
                                        'end_date': f'{str(int(to_year))}-01-01',
                                        'train_size': train_size_value/100,
                                        'test_size': test_size_value/100,
                                        'deploy_size': 0.0
                                    }
                                    response = requests.get(
                                        f'http://127.0.0.1:8000/setups/{model.lower()}_model/fit', json=json)

                                    if response.status_code == 200:
                                        r_summary = requests.get(
                                            'http://127.0.0.1:8000/setups/svr_model/', json={'name': ativo})
                                        model_summary = r_summary.json()[
                                            'summary']

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
