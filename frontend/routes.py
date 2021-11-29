import streamlit as st
from pages.index import BTKApp

st.set_page_config(
    page_title='BTK App',
    layout='wide'
)

if "is_logged" not in st.session_state:
    st.session_state.is_logged = False

pagina = BTKApp(st.session_state.is_logged)
pagina.home(st=st)