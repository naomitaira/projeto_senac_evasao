import streamlit as st
import pandas as pd
import openpyxl 


st.title("Evasão escolar de São Paulo")


df_abandono_2022 = pd.read_excel("sp/dados_limpos/total_abandono_escolar_2022_excel.xlsx")
df_abandono_2023 = pd.read_excel("sp/dados_limpos/total_abandono_escolar_2023_excel.xlsx")
df_abandono_2024 = pd.read_excel("sp/dados_limpos/total_abandono_escolar_2024_excel.xlsx")

# criacao de colunas para exibir os dados de cada ano lado a lado
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("2022")
    st.dataframe(df_abandono_2022)
with col2:
    st.subheader("2023")
    st.dataframe(df_abandono_2023)
with col3:
    st.subheader("2024")
    st.dataframe(df_abandono_2024)


