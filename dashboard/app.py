#script página dashboard evasão

import streamlit as st

#configura a página do streamlit com título, ícone e layout
st.set_page_config(
    page_title = 'Dashboard Evasão Escolar',
    page_icon = '📊',
    layout= 'wide'
)

#define as páginas do menu
dashboard_evasao = st.Page("pages/dashboard_evasao.py",
                           title='Dashboard Evasão EScolar',
                           #icon='',
                           default=True)


#cria o menu lateral para navegação entre as páginas
menu = st.navigation(
    [dashboard_evasao]
)