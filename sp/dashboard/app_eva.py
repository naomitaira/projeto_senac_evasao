import streamlit as st

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
    background-color: #FFF0F5;
}
</style>
""", unsafe_allow_html=True)


# configura a pagina do streamlit
st.set_page_config(
    page_title="Projeto Evasão Escolar",
    page_icon="📚",
    layout="wide"
)

# define paginas do menu
paginas_sp = st.Page(
    "page_sp.py", title="Evasão escolar de São Paulo", icon="📌") 

paginas_mapa= st.Page(
    "page_mapa.py", title="Mapa de evasão escolar", icon="🗺️")


# cria menu lateral para navegacao entre paginas

menu = st.navigation(
    [paginas_sp, paginas_mapa])


menu.run()

