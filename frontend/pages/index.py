import streamlit as st

from .btk_main_app import BTKMainApp
from .login import LoginApp

from .long_and_short_app import LongAndShortApp

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
            st.header('BTK App')
            st.sidebar.header('Sidebar BTK App')
            BTKMainApp().home(st=st)

            # if st.sidebar.button('Log Out'):
            #     print(
            #         f"Session State LogOutBefore: {st.session_state.is_logged}")
            #     st.session_state.is_logged = False
            #     st.experimental_rerun()
            #     st.stop()
            #     print(
            #         f"Session State LogOutAfter: {st.session_state.is_logged}")
