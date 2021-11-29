import streamlit as st

from pages.risk_management_app import RiskManagementApp
from pages.btk_predict_app import PredictionApp
from pages.stock_monitor_app import StockMonitorApp
from pages.login import LoginApp

import requests
import json

class BTKApp:
    def __init__(self, logged):
        if not logged:
            self.login = LoginApp()
            return
        
    def home(self, st):
        page = None

        if st.session_state.is_logged == False:
            self.login.home(st=st)
                    
        if st.session_state.is_logged:
            st.header('BTK App 🏄🏻‍♂️')
            PredictionApp().home(st=st)

            if st.sidebar.button('Log Out'):
                print(f"Session State LogOutBefore: {st.session_state.is_logged}")
                st.session_state.is_logged = False
                st.experimental_rerun()
                st.stop()
                print(f"Session State LogOutAfter: {st.session_state.is_logged}")