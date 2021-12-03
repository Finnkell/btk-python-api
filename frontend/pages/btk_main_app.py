from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split

from .ai_models_app import AIModelsApp

from .long_and_short_app import LongAndShortApp

import joblib
import requests
import yfinance as yf
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


class BTKMainApp:

    def home(self, st):

        analysis = st.sidebar.selectbox('Quais tipos de análises você deseja ver?', (
            'Página inicial', 'Modelos de IA', 'Estratégias L&S', 'Markowitz'))

        if analysis != 'Página inicial':
            if analysis == 'Modelos de IA':
                AIModelsApp().home(st=st)
            elif analysis == 'Estratégias L&S':
                LongAndShortApp().home(st=st)
            elif analysis == 'Markowitz':
                pass
        else:
            st.markdown('Este é um aplicativo que mostra os sinais de estratégias e modelos de inteligência artificial hospedados dentro da BTK A.Intelligence.\n\n Ele tem por objetivo ser um ferramenta para auxiliar nos investimentos em um determinado ativo ou cesta de ativos.')
