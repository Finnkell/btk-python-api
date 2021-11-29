import pandas as pd
import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go

class StockMonitorApp:
    
    def home(self, st):
        @st.cache
        def load_json():
            return pd.read_json('static/stocks.json')

        @st.cache(allow_output_mutation=True)
        def load_data(ticket, year):
            if '-' not in ticket and (ticket.endswith('3') or ticket.endswith('4') or ticket.endswith('5') or ticket.endswith('6') or ticket.endswith('11') or ticket.endswith('34')):
                ticket = ticket + '.SA'
                return yf.download(ticket, start=f'{year}-01-01')

            return yf.download(ticket, start=f'{year}-01-01') 

        def show_indicator_chart(data, indicator):
            if indicator == 'SMA':
                data['SMA'] = data['Close'].rolling(window=10).mean()

                fig = go.Figure()
                fig.add_traces([
                    go.Scatter(y=data['Close'], mode='lines', name='close'),
                    go.Scatter(y=data['SMA'], mode='lines', name='SMA'),
                ])
                fig.update_layout(template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)


        def show_info(asset, year, indicator, st):
            data = load_data(asset, year)

            st.subheader(asset)

            if indicator:
                show_indicator_chart(data, indicator)
            else:
                fig = px.line(data['Close'])
                fig.update_layout(template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)

            if data['Close'].iloc[-1] < data['Close'].iloc[-7]:
                volatility = data['Close'].iloc[-7:].pct_change().std() * np.sqrt(252)
                returns = data['Close'].iloc[-7:].pct_change().mean() * 252   

                metrics = {
                    'volatility': volatility,
                    'return': returns,
                }

                st.error('Ativo em baixa')

                for key in metrics:  
                    st.write(f'{key}: ', round(metrics[key], 4))

            else:
                volatility = data['Close'].pct_change().std() * np.sqrt(252)
                returns = data['Close'].pct_change().mean() * 252

                metrics = {
                    'volatility': volatility,
                    'return': returns,
                }

                st.success('Ativo em alta')

                for key in metrics:  
                    st.write(f'{key}: ', round(metrics[key], 4))
                
            with st.expander('Detalhes'):
                st.subheader('Últimos 10 dias do ativo')
                st.dataframe(data.tail(10))


        assets_json = load_json()
        assets_select = (assets_json['stocks'])

        st.header('BTK Stock monitor para a avaliação de ativos no mercado de capitais')

        assets = st.sidebar.multiselect('Qual ativo?', assets_select)

        col1, col2 = st.columns(2)

        if assets:
            indicators = st.sidebar.multiselect('Qual indicador?', ('SMA', 'BB', 'RSI'))
            year = st.sidebar.slider('Desde qual ano?', 2019, 2021)

            for asset, count in zip(assets, range(len(assets))):
                if indicators:
                    for indicator in indicators:
                        if count % 2 == 0:
                            with col1:
                                show_info(asset, year, indicator, st)
                        else:
                            with col2:
                                show_info(asset, year, indicator, st)
                else:
                    if count % 2 == 0:
                        with col1:
                            show_info(asset, year, '', st)
                    else:
                        with col2:
                            show_info(asset, year, '', st)



