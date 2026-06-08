from page_sp import carregar_dados
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
from utils_dados import carregar_dados

# ============================
# CONFIGURAÇÃO
# ============================

st.set_page_config(layout="wide")
st.title("Comparativo de Evasão Escolar (2022-2024)")

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[2]

LOCAL_GEOJSON_PATH = CURRENT_DIR / "brazil_municipios.geojson"
LOCAL_IBGE_MUNICIPIOS_PATH = CURRENT_DIR / "ibge_municipios.csv"

if not LOCAL_GEOJSON_PATH.exists():
    LOCAL_GEOJSON_PATH = ROOT_DIR / "sp" / "dashboard" / "brazil_municipios.geojson"

if not LOCAL_IBGE_MUNICIPIOS_PATH.exists():
    LOCAL_IBGE_MUNICIPIOS_PATH = ROOT_DIR / "sp" / "dashboard" / "ibge_municipios.csv"

REGIONAL_DATA_PATH = ROOT_DIR / "dados_evasao" / "AbandonoEscolar_RendaMedia_2013_2023.csv"

motivos_df = None

# ============================
# FUNÇÕES
# ============================

def load_abandono_csv(path: Path, year: int) -> pd.DataFrame:
    df = pd.read_csv(path, sep=';', decimal=',', encoding='utf-8', engine='python')

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df.columns = [c.strip() for c in df.columns]

    municipio_col = next((c for c in df.columns if "munic" in c.lower()), None)
    abandono_col = next((c for c in df.columns if "aband" in c.lower()), None)

    if municipio_col is None or abandono_col is None:
        raise ValueError(f"Colunas não encontradas em {path.name}")

    df = df[[municipio_col, abandono_col]].copy()
    df.columns = ["Municipio", "Taxa"]

    df["Taxa"] = pd.to_numeric(df["Taxa"], errors="coerce")
    df = df.dropna(subset=["Taxa"])
    df["Year"] = year

    return df


def load_all(dados_dir: Path):
    arquivos = {
        2022: dados_dir / "total_abandono_escolar_2022.csv",
        2023: dados_dir / "total_abandono_escolar_2023.csv",
        2024: dados_dir / "total_abandono_escolar_2024.csv"
    }

    dfs = []
    for ano, arquivo in arquivos.items():
        if arquivo.exists():
            try:
                dfs.append(load_abandono_csv(arquivo, ano))
            except Exception as e:
                st.warning(f"Erro ao carregar {arquivo.name}: {e}")

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def load_region_abandono(path: Path):
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path, sep=',', encoding='utf-8', engine='python')

    df = df[
        (df["Regiao"] == "Brasil")
        & (df["Localizacao"] == "Total")
        & (df["Dependencia_Administrativa"] == "Total")
        & (df["Grupo_de_Abandono"] == "Ensino Fundamental")
    ].copy()

    df["Unidade_Geografica"] = df["Unidade_Geografica"].astype(str).str.strip()
    df["Taxa_Abandono"] = pd.to_numeric(df["Taxa_Abandono"], errors="coerce")

    df = df[df["Unidade_Geografica"].notnull() & df["Unidade_Geografica"] != ""]

    return df


# ============================
# CARREGAR DADOS
# ============================

DATA_DIR = Path("/Documents/projeto_senac_evasao/dados_tratados")
df_all = load_all(DATA_DIR)

if df_all.empty:
    st.error(f"Nenhum dado encontrado em {DATA_DIR}")
    st.stop()

# ============================
# SIDEBAR (DEFININDO VARIÁVEIS PRIMEIRO)
# ============================
BASE_DIR = "sp/dados_limpos"
abandono, df_all = None, carregar_dados(BASE_DIR)

if df_all.empty:
    st.warning("Arquivos não encontrados. Rode o script de processamento ")
    st.stop()
with st.sidebar:
    st.header("Filtros")

    ano_metricas = st.selectbox(
        "Ano das métricas",
        sorted(df_all["Year"].unique(), reverse=True)
    )

    municipios = sorted(df_all["Municipio"].unique())

    default_sel = (
        df_all.groupby("Municipio")["Taxa"]
        .mean()
        .sort_values(ascending=False)
        .head(8)
        .index
        .tolist()
    )

    sel_mun = st.multiselect(
        "Selecione municípios",
        municipios,
        default=default_sel
    )

    st.markdown("---")

    st.write("Upload opcional de motivos de evasão")
    motivos_upload = st.file_uploader("CSV com colunas Municipio e Motivo")

    motivos_path = ROOT_DIR / "dados_tratados" / "motivos_evasao.csv"

    if motivos_upload is not None:
        try:
            motivos_df = pd.read_csv(motivos_upload, encoding='utf-8')
            st.success("Arquivo de motivos carregado com sucesso.")
        except Exception as e:
            st.warning(f"Não foi possível ler o arquivo de motivos: {e}")
            motivos_df = None

    elif motivos_path.exists():
        try:
            motivos_df = pd.read_csv(motivos_path, encoding='utf-8')
            st.info("Arquivo de motivos encontrado localmente e carregado.")
        except Exception as e:
            st.warning(f"Erro ao ler motivos locais: {e}")
            motivos_df = None

    st.markdown("---")

    resumo = df_all.groupby("Year")["Taxa"].mean().reset_index()
    st.write("Resumo anual")
    st.dataframe(resumo, hide_index=True)

# ============================
# MÉTRICAS (AGORA FUNCIONA)
# ============================

df_metrics = df_all[df_all["Year"] == ano_metricas]

col1, col2, col3 = st.columns(3)

col1.metric("Municípios", df_metrics["Municipio"].nunique())
col2.metric("Taxa Média", f"{df_metrics['Taxa'].mean():.2f}%")
col3.metric("Maior Taxa", f"{df_metrics['Taxa'].max():.2f}%")

st.caption(f"Métricas calculadas para o ano {ano_metricas}.")
