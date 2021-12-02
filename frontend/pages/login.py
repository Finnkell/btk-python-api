import requests
import json

from pages.register import RegisterApp

class LoginApp:
    def __init__(self):
        self.__email = ''
        self.__pass = ''
        
        self.__register_app = RegisterApp()

    def home(self, st):
        if st.session_state.w_register:
            self.__register_app.home(st=st)
           
        if not st.session_state.w_register:
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
                        
            if st.button('Criar conta'):
                st.session_state.w_register = True
                st.experimental_rerun()

    def handle_login(self, user, password):
        status = ''

        response = requests.post('http://127.0.0.1:8000/auth/login', data=json.dumps(
            {"cpf": user, "password": str(password)}), headers={'content-type': 'application/json'})

        status = response.status_code

        if status:
            return status
        else:
            return None
