from page_sp import carregar_dados
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
    page_icon="✎",
    layout="wide"
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #E6E6FA;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
<style>
.stApp {
    background-color: #8FDC9F;
}
</style>
""", unsafe_allow_html=True)
# define paginas do menu
paginas_sp = st.Page(
    "page_sp.py",
    title="Evasão escolar de São Paulo",
    icon="🎒"
)

paginas_comparativo = st.Page(
    "page_comp.py",
    title="Comparativo de evasão escolar",
    icon="📚"
)

paginas_comparativo_atualizado = st.Page(
    "page_map_comp.py",
    title="Comparativo de evasão escolar atualizado",
    icon="🗺️"
)


# cria menu lateral para navegacao entre paginas

menu = st.navigation(
    [paginas_sp, paginas_comparativo, paginas_comparativo_atualizado])


menu.run()