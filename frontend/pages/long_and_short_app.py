import pandas as pd


class LongAndShortApp:

    def home(self, st):
        @st.cache()
        def load_data(self, stock):
            return yf.download(stock)

        st.header('Long & Short App')

        ativo = st.sidebar.select(
            'Quais pares?', ('PETR4/PETR3', 'ITUB4/ITUB3'))

        stocks_correlation = requests.get(
            '', json={'name': ativo}).json()['correlation']

        for stocks in stocks_correlation:
            pass
