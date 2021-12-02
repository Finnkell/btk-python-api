import requests
import json
import random


class RegisterApp:
    def __init__(self):
        self.__cpf = ''
        self.__password1 = ''
        self.__username = ''
        self.__email = ''
        self.__phone = ''
        
    def home(self, st):
        with st.form(key='Register', clear_on_submit=False):
            st.header('Criar conta')
            
            self.__username = st.text_input('Nome Completo')
            self.__email = st.text_input('Email')
            self.__cpf = st.text_input('CPF')
            self.__password1 = st.text_input('Senha', type='password')
            
            self.__phone = st.text_input('Telefone')

            submitted = st.form_submit_button('CRIAR CONTA')

            if submitted:
                status = self.handle_login(user=self.__username, email=self.__email, password=self.__password1, cpf=self.__cpf, phone=self.__phone)

                if status == 201:
                    st.session_state.w_register = False
                    st.experimental_rerun()
                else:
                    st.session_state.is_logged = False
        
    def handle_login(self, user, password, email, cpf, phone):
        status = ''

        response = requests.post('http://127.0.0.1:8000/auth/register/', data=json.dumps(
            {"cpf": cpf, "password": str(password), "username": user, "email": email, "phone": phone}), headers={'content-type': 'application/json'})

        status = response.status_code

        if status:
            return status
        else:
            return