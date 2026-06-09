import streamlit as st
import pandas as pd
import plotly.express as px
import json
import re
import unicodedata
from pathlib import Path
from utils_dados import carregar_dados

st.set_page_config(layout="wide")
st.title("Mapa de Evasão Escolar (2022-2024) 📈")

ROOT_DIR = Path(__file__).resolve().parents[1]

GEOJSON_PATH = ROOT_DIR / "dashboard/geojs-sao-paulo.json"
IBGE_PATH = ROOT_DIR / "dashboard/ibge_municipios.csv"
DATA_DIR = ROOT_DIR / "dados_tratados"


def normalize(text):
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKD", text.upper())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]", " ", text)).strip()


def carregar_abandono():
    arquivos = {
        2022: "total_abandono_escolar_2022.csv",
        2023: "total_abandono_escolar_2023.csv",
        2024: "total_abandono_escolar_2024.csv"
    }

    dfs = []

    for ano, nome in arquivos.items():

        arquivo = DATA_DIR / nome

        if not arquivo.exists():
            continue

        df = pd.read_csv(
            arquivo,
            sep=";",
            decimal=",",
            encoding="utf-8"
        )

        municipio = next(
            c for c in df.columns
            if "munic" in c.lower()
        )

        taxa = next(
            c for c in df.columns
            if "aband" in c.lower()
        )

        df = df[[municipio, taxa]].copy()

        df.columns = ["Municipio", "Taxa"]
        df["Taxa"] = pd.to_numeric(
            df["Taxa"],
            errors="coerce"
        )

        df["Year"] = ano

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


# ---------------- DADOS ----------------

df_all = carregar_abandono()

df_ibge = pd.read_csv(
    IBGE_PATH,
    dtype={"id": str}
)

df_ibge = df_ibge[
    df_ibge["id"].str.startswith("35")
]

df_all["nome_norm"] = (
    df_all["Municipio"]
    .map(normalize)
)

df_ibge["nome_norm"] = (
    df_ibge["nome"]
    .map(normalize)
)

df_infra = carregar_dados("sp/dados_limpos")

with st.sidebar:

    ano = st.selectbox(
        "Ano",
        sorted(df_all["Year"].unique(),
               reverse=True)
    )

# ---------------- MÉTRICAS ----------------

df_ano = df_all[
    df_all["Year"] == ano
]

media_evasao = df_ano["Taxa"].mean()

delta = None

if ano - 1 in df_all["Year"].unique():

    delta = (
        media_evasao -
        df_all[
            df_all["Year"] == ano - 1
        ]["Taxa"].mean()
    )

# infraestrutura

infra_ano = df_infra[
    df_infra["Ano"] == ano
].copy()

cols_acesso = [
    c for c in infra_ano.columns
    if "ACESSO" in normalize(c)
]

for c in cols_acesso:
    infra_ano[c] = pd.to_numeric(
        infra_ano[c],
        errors="coerce"
    )

media_infra = infra_ano[
    cols_acesso
].mean()

melhor = media_infra.idxmax()
pior = media_infra.idxmin()

k1, k2, k3 = st.columns(3)

k1.metric(
    "Taxa média de evasão",
    f"{media_evasao:.2f}%",
    f"{delta:+.2f}pp" if delta is not None else None
)

k2.metric(
    "Infra mais desenvolvida",
    melhor,
    f"{media_infra.max():.1f}%"
)

k3.metric(
    "Infra mais deficiente",
    pior,
    f"{media_infra.min():.1f}%"
)

# ---------------- MAPA ----------------

geojson = json.loads(
    GEOJSON_PATH.read_text(
        encoding="utf-8"
    )
)

df_map = (
    pd.merge(
        df_ano,
        df_ibge[["id", "nome_norm"]],
        on="nome_norm",
        how="inner"
    )
    .groupby("id", as_index=False)
    ["Taxa"]
    .mean()
)

df_map["id"] = df_map["id"].astype(str)

fig = px.choropleth_mapbox(
    df_map,
    geojson=geojson,
    locations="id",
    featureidkey="properties.id",
    color="Taxa",
    color_continuous_scale="Purples",
    mapbox_style="carto-positron",
    center={"lat": -22.0, "lon": -48.0},
    zoom=6,
    opacity=0.7
)

fig.update_layout(
    margin=dict(
        r=0,
        t=0,
        l=0,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)