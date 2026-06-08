import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path

st.set_page_config(layout="wide")

st.title("Mapa do Censo Escolar por Município")

# ==========================
# Caminhos
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "dados_evasao"
GEOJSON_PATH = BASE_DIR / "dashboard" / "brazil_municipios.geojson"

ARQUIVOS = {
    2022: DATA_DIR / "censo_escolar_brasil_2022.xlsx",
    2023: DATA_DIR / "censo_escolar_brasil_2023.xlsx",
    2024: DATA_DIR / "censo_escolar_brasil_2024.xlsx",
}

# ==========================
# Seleção do ano
# ==========================

ano = st.sidebar.selectbox(
    "Selecione o ano",
    [2022, 2023, 2024],
    index=2
)

arquivo_excel = ARQUIVOS[ano]

if not arquivo_excel.exists():
    st.error(f"Arquivo não encontrado:\n{arquivo_excel}")
    st.stop()

if not GEOJSON_PATH.exists():
    st.error(f"GeoJSON não encontrado:\n{GEOJSON_PATH}")
    st.stop()

# ==========================
# Leitura do Excel
# ==========================

df = pd.read_excel(arquivo_excel)

st.sidebar.markdown("### Configuração")

codigo_col = st.sidebar.selectbox(
    "Coluna do código IBGE",
    df.columns
)

valor_col = st.sidebar.selectbox(
    "Coluna para exibir no mapa",
    df.columns
)

# ==========================
# Tratamento
# ==========================

df["cod_ibge"] = (
    df[codigo_col]
    .astype(str)
    .str.replace(r"\D", "", regex=True)
    .str.zfill(7)
)

df["valor"] = pd.to_numeric(
    df[valor_col],
    errors="coerce"
)

df = df.dropna(subset=["valor"])

# Caso existam registros repetidos por município
df = (
    df.groupby("cod_ibge", as_index=False)["valor"]
    .mean()
)

# ==========================
# GeoJSON
# ==========================

with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Mostra as propriedades disponíveis
propriedades = list(
    geojson["features"][0]["properties"].keys()
)

campo_geojson = st.sidebar.selectbox(
    "Campo do GeoJSON",
    propriedades
)

# ==========================
# Mapa
# ==========================

fig = px.choropleth(
    df,
    geojson=geojson,
    locations="cod_ibge",
    featureidkey=f"properties.{campo_geojson}",
    color="valor",
    color_continuous_scale="OrRd",
    title=f"Mapa do Censo Escolar - {ano}"
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Prévia dos dados
# ==========================

with st.expander("Visualizar dados"):
    st.dataframe(df.head(20))