# import streamlit as st
import requests
import json
import random


class LoginApp:
    def __init__(self):
        self.__email = ''
        self.__pass = ''

    def home(self, st):
        with st.form(key='login', clear_on_submit=False):
            st.header('Login')

            self.__email = st.text_input('Cpf')
            self.__password = st.text_input('Password', type='password')

            submitted = st.form_submit_button('Login')

            if submitted:
                status = self.handle_login(self.__email, self.__password)

                if status == 200:
                    st.session_state.is_logged = True
                    st.experimental_rerun()
                else:
                    st.session_state.is_logged = False

    def handle_login(self, user, password):
        status = ''

        response = requests.post('http://127.0.0.1:8000/auth/login', data=json.dumps(
            {"cpf": user, "password": str(password)}), headers={'content-type': 'application/json'})

        status = response.status_code

        if status:
            return status
        else:
            return