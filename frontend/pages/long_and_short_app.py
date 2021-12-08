import pandas as pd
import numpy as np
import yfinance as yf

DF = ['PETR3/PETR4', 'ITUB3/ITUB4']
DIVISAO = ['LAME3/LAME4', 'ITSA3/ITSA4' ]
CORRELACAO = ['BBDC3/BBDC4']

class LongAndShortApp:
    def __init__(self):
        pass

    def home(self, st):
        
        @st.cache(allow_output_mutation=True)
        def load_data(option, from_year='', to_year=''):
            if from_year == '' or to_year == '':
                return yf.download(option)

            return yf.download(option, start=f'{from_year}-01-01', end=f'{to_year}-01-01')

        st.sidebar.header('Método para Simulação')
        metodos = st.sidebar.multiselect('Qual método?', ('DF', 'DIVISÃO', 'CORRELAÇÃO'))

        ativos = ['---']

        if 'DF' in metodos:
            ativos += DF

        if 'DIVISÃO' in metodos:
            ativos += DIVISAO

        if 'CORRELAÇÃO' in metodos:
            ativos += CORRELACAO

        if not 'DF' in metodos:
            if DF in ativos:
                ativos -= DF

        if not 'DIVISÃO' in metodos:
            if DIVISAO in ativos:
                ativos -= DIVISAO

        if not 'CORRELAÇÃO' in metodos:
            if CORRELACAO in ativos:
                ativos -= CORRELACAO

        asset_select = st.sidebar.selectbox('Escolha um par de ativos', ativos)

        if ativos:
            st.subheader('Estratégias L&S')

            ativos = str(asset_select).split('/')

            if ativos[0] != '---':
                st.subheader(f'{ativos[0]}')
                st.line_chart(load_data(f'{ativos[0]}.SA')['Close'].dropna())

                st.subheader(f'{ativos[1]}')
                st.line_chart(load_data(f'{ativos[1]}.SA')['Close'].dropna())

                data1 = load_data(f'{ativos[0]}.SA')['Close']
                data2 = load_data(f'{ativos[1]}.SA')['Close']
                data = data1.fillna(data2.mean())/data2.fillna(data2.mean())
                
                table_metodo = ''
                for i in metodos:
                    table_metodo += i + " e "
                    
                table_metodo = table_metodo[:len(table_metodo) - 2]
                
                df_atv_table = pd.DataFrame( np.array([[table_metodo, asset_select, '2.0', '0.96', '1.08']]),
                                columns=['Métodos', 'Par', 'Desvio Padrão', 'Stop-Loss', 'Take-Profit'])

                st.table(df_atv_table)

                st.subheader(f'{ativos[0]}/{ativos[1]}')
                st.line_chart(data)
                st.subheader('Banca')

                df = pd.DataFrame( np.array([[ativos[0], 'VENDA', '30%'], [ativos[1], 'COMPRA', '60%']]),
                                    columns=['ATIVO', 'OPERAÇÃO', 'PORCENTAGEM'])

                df.set_index('ATIVO')

                st.table(df)
                st.subheader(f'Backtest iniciado com R$10.000')
                st.area_chart([10, 2, 7, 20, 15, 30, 22, 19, 6, 50, 100])
                
            else:
                st.markdown('Selecione os métodos e escolha o par para visualizar a estratégia de Pairs Trading ')
