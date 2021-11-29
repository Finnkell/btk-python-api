import pandas as pd
import yfinance as yf

# from tools.markowitz import Markowitz
# from tools.expected_shortfall import ExpectedShortfall
# from tools.value_at_risk import ValueAtRisk

class RiskManagementApp:

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

        window_option = st.sidebar.selectbox('Método', ('Expected Shortfall', 'Markowitz', 'Value at Risk'))

        if window_option == 'Markowitz':
            st.header('Método de Markowitz')
            
            qtd_ativos = st.sidebar.text_input('Quantidade de ativos')

            if qtd_ativos != '':
                for i in range(int(qtd_ativos)):
                    st.sidebar.selectbox(f'Ativo {i}', tickets)
            st.write(Markowitz())

        elif window_option == 'Expected Shortfall':
            st.header('Método de Expected Shortfall')
            st.write(ExpectedShortfall())

        elif window_option == 'Value at Risk':
            st.header('Método de Value at Risk')
            st.write(ValueAtRisk())