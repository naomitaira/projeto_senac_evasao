import streamlit as st
from utils_dados import carregar_dados

BASE_DIR = "sp/dados_limpos"
abandono, df_all = None, carregar_dados(BASE_DIR)

if df_all.empty:
    st.warning("Arquivos não encontrados. Rode o script de processamento primeiro.")
    st.stop()
# configura a pagina do streamlit
st.set_page_config(
    page_title="Projeto Evasão Escolar",
    page_icon="🏫",
    layout="wide"
)

# personaliza cor da barra lateral
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #AFC4D5;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# personaliza cor do fundo da pagina
st.markdown("""
<style>
.stApp {
    background-color: #F4F6F8;
}
</style>
""", unsafe_allow_html=True)

# personaliza cor das tags
st.markdown("""
<style>
span[data-baseweb="tag"] {
  background-color: #D7C8E8 !important;
}
</style>
""", unsafe_allow_html=True) #colocar antes dos filtros pra dar cor

# define paginas do menu
paginas_sp = st.Page(
    "page_sp.py",
    title="Evasão escolar de São Paulo",
    icon="🎒"
)

paginas_mapa = st.Page(
    "page_mapa.py",
    title="Mapa de evasão escolar",
    icon="🗺️"
)

# cria menu lateral para navegacao entre paginas

menu = st.navigation(
    [paginas_sp, paginas_mapa])


menu.run()