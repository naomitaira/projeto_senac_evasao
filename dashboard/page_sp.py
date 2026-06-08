import streamlit as st
import pandas as pd
from utils_dados import carregar_dados
import os 

st.markdown("""
<style>
    h1, h2, h3, h4, h5, h6,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] { 
        color: black !important; 
    }
</style>
""", unsafe_allow_html=True)
st.title("Evasão Escolar — São Paulo ✵")
st.divider()
COLUNAS_INFRA = [
    'Acesso à internet para alunos',
    'Acesso ao Laboratório de informática',
    'Acesso à Biblioteca',
    'Acesso à Alimentação',
    'Acesso ao Refeitório',
    'Acesso à Água potável',
    'Acesso à Energia elétrica da rede pública',
    'Acesso à Esgoto da rede pública',
    'Acesso ao Banheiro',
    'Acesso à Quadra de esportes',
]

INFRA_LABELS = {
    col: label for col, label in zip(
        COLUNAS_INFRA,
        ['Internet', 'Lab. Informática', 'Biblioteca', 'Alimentação', 'Refeitório',
         'Água Potável', 'Energia Elétrica', 'Esgoto', 'Banheiro', 'Quadra de Esportes']
    )
}
@st.cache_data
def carregar_dados():
    abandono = {
        ano: pd.read_excel(f"sp/dados_limpos/total_abandono_escolar_{ano}_excel.xlsx")
        for ano in [2022, 2023, 2024]
    }

    frames = []
    for ano in abandono:
        path = f"sp/dados_limpos/relacao_evasao_infraestrutura_{ano}.xlsx"
        if os.path.exists(path):
            df = pd.read_excel(path)
            df['Ano'] = ano
            df['Total Abandono Escolar'] = pd.to_numeric(df['Total Abandono Escolar'], errors='coerce')
            frames.append(df)

    return abandono, pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
abandono, df_all = carregar_dados()
if df_all.empty:
    st.warning("Arquivos não encontrados. Rode o script de processamento primeiro.")
    st.stop()
st.text("Selecione o ano, número de municípios e infraestrutura para análise:")

col_f1, col_f2, col_f3 = st.columns(3)
ano_sel = col_f1.selectbox("Ano", sorted(df_all['Ano'].unique(), reverse=True))
n_top = col_f2.selectbox("Top municípios", [5, 10, 15, 20], index=1)
infra_cor = col_f3.selectbox("Infraestrutura", COLUNAS_INFRA, )

st.divider()
df_ano = df_all[df_all['Ano'] == ano_sel]
anos_disp = sorted(df_all['Ano'].unique())
media_atual = df_ano['Total Abandono Escolar'].mean()
media_ant = df_all[df_all['Ano'] == ano_sel - 1]['Total Abandono Escolar'].mean() if ano_sel - 1 in anos_disp else None
delta = media_atual - media_ant if media_ant else None

pior_mun = df_ano.loc[df_ano['Total Abandono Escolar'].idxmax(), 'Municipio']
pior_val = df_ano['Total Abandono Escolar'].max()

media_infra = df_ano[COLUNAS_INFRA].mean()
pior_infra_col = media_infra.idxmin()

k1, k2, k3 = st.columns(3)
k1.metric("Taxa média de evasão", f"{media_atual:.2f}%", delta=f"{delta:+.2f}" if delta else None)
k2.metric("Maior evasão", f"{pior_val:.1f}%", delta=pior_mun.title())
k3.metric("Infra mais deficiente", INFRA_LABELS[pior_infra_col])

st.divider()
