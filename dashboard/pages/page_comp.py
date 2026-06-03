import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
import unicodedata

CURRENT_DIR = Path(__file__).resolve().parent
SP_DASHBOARD_DIR = Path(__file__).resolve().parents[2] / "sp" / "dashboard"

LOCAL_GEOJSON_PATH = CURRENT_DIR / "brazil_municipios.geojson"
LOCAL_IBGE_MUNICIPIOS_PATH = CURRENT_DIR / "ibge_municipios.csv"
if not LOCAL_GEOJSON_PATH.exists():
    LOCAL_GEOJSON_PATH = SP_DASHBOARD_DIR / "brazil_municipios.geojson"
if not LOCAL_IBGE_MUNICIPIOS_PATH.exists():
    LOCAL_IBGE_MUNICIPIOS_PATH = SP_DASHBOARD_DIR / "ibge_municipios.csv"

REGIONAL_DATA_PATH = Path(__file__).resolve().parents[2] / "dados_evasao" / "AbandonoEscolar_RendaMedia_2013_2023.csv"

motivos_df = None

st.set_page_config(layout="wide")

st.title("Comparativo de Evasão Escolar (2022-2024)")

st.markdown("""
Nesta seção, apresentamos um comparativo da evasão escolar entre os anos de 2022, 2023 e 2024.
Selecione municípios para comparar taxas e explore distribuições e rankings.
""")


# ==========================
# FUNÇÃO DE LEITURA
# ==========================

def load_abandono_csv(path: Path, year: int) -> pd.DataFrame:

    df = pd.read_csv(
        path,
        sep=';',
        decimal=',',
        encoding='utf-8',
        engine='python'
    )

    # Remove coluna índice criada pelo pandas
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Limpa nomes das colunas
    df.columns = [c.strip() for c in df.columns]

    # Encontrar coluna de município
    municipio_col = next(
        (c for c in df.columns if "munic" in c.lower()),
        None
    )

    # Encontrar coluna de abandono
    abandono_col = next(
        (
            c for c in df.columns
            if "aband" in c.lower()
        ),
        None
    )

    if municipio_col is None or abandono_col is None:
        raise ValueError(
            f"Colunas não encontradas em {path.name}"
        )

    df = df[[municipio_col, abandono_col]].copy()

    df.columns = [
        "Municipio",
        "Taxa"
    ]

    df["Taxa"] = pd.to_numeric(
        df["Taxa"],
        errors="coerce"
    )

    df = df.dropna(subset=["Taxa"])

    df["Year"] = year

    return df


# ==========================
# CARREGAR TODOS OS ARQUIVOS
# ==========================

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
                dfs.append(
                    load_abandono_csv(
                        arquivo,
                        ano
                    )
                )

            except Exception as e:
                st.warning(
                    f"Erro ao carregar {arquivo.name}: {e}"
                )

    if dfs:
        return pd.concat(
            dfs,
            ignore_index=True
        )

    return pd.DataFrame()


STATE_TO_REGION = {
    "11": "Norte", "12": "Norte", "13": "Norte", "14": "Norte", "15": "Norte", "16": "Norte", "17": "Norte",
    "21": "Nordeste", "22": "Nordeste", "23": "Nordeste", "24": "Nordeste", "25": "Nordeste", "26": "Nordeste", "27": "Nordeste", "28": "Nordeste", "29": "Nordeste",
    "31": "Sudeste", "32": "Sudeste", "33": "Sudeste", "35": "Sudeste",
    "41": "Sul", "42": "Sul", "43": "Sul",
    "50": "Centro-Oeste", "51": "Centro-Oeste", "52": "Centro-Oeste", "53": "Centro-Oeste",
}


def load_region_abandono(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(
        path,
        sep=',',
        encoding='utf-8',
        engine='python'
    )

    df = df[
        (df["Regiao"] == "Brasil")
        & (df["Localizacao"] == "Total")
        & (df["Dependencia_Administrativa"] == "Total")
        & (df["Grupo_de_Abandono"] == "Ensino Fundamental")
    ].copy()

    df["Unidade_Geografica"] = df["Unidade_Geografica"].astype(str).str.strip()
    df["Taxa_Abandono"] = pd.to_numeric(df["Taxa_Abandono"], errors="coerce")
    df = df[df["Unidade_Geografica"].isin([
        "Norte",
        "Nordeste",
        "Centro-Oeste",
        "Sudeste",
        "Sul"
    ])]

    return df


# ==========================
# DIRETÓRIO DOS DADOS
# ==========================

DATA_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "dados_tratados"
)

df_all = load_all(DATA_DIR)

if df_all.empty:
    st.error(
        f"Nenhum dado encontrado em {DATA_DIR}"
    )
    st.stop()


# ==========================
# MÉTRICAS
# ==========================

df_metrics = df_all[df_all["Year"] == ano_metricas]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Municípios",
        df_metrics["Municipio"].nunique()
    )

with col2:
    st.metric(
        "Taxa Média",
        f"{df_metrics['Taxa'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Maior Taxa",
        f"{df_metrics['Taxa'].max():.2f}%"
    )

st.caption(f"Métricas calculadas para o ano {ano_metricas}.")


# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.header("Filtros")

    ano_metricas = st.selectbox(
        "Ano das métricas",
        sorted(df_all["Year"].unique(), reverse=True)
    )

    municipios = sorted(
        df_all["Municipio"].unique()
    )

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
    motivos_upload = st.file_uploader(
        "CSV com colunas Municipio e Motivo",
        type=["csv"]
    )

    motivos_path = Path(__file__).resolve().parents[2] / "dados_tratados" / "motivos_evasao.csv"
    if motivos_upload is not None:
        try:
            motivos_df = pd.read_csv(
                motivos_upload,
                encoding='utf-8',
                engine='python'
            )
            st.success("Arquivo de motivos carregado com sucesso.")
        except Exception as e:
            st.warning(f"Não foi possível ler o arquivo de motivos: {e}")
            motivos_df = None
    elif motivos_path.exists():
        try:
            motivos_df = pd.read_csv(
                motivos_path,
                encoding='utf-8',
                engine='python'
            )
            st.info("Arquivo de motivos encontrado localmente e carregado.")
        except Exception as e:
            st.warning(f"Erro ao ler motivos locais: {e}")
            motivos_df = None
    else:
        motivos_df = None

    st.markdown("---")

    resumo = (
        df_all.groupby("Year")["Taxa"]
        .mean()
        .reset_index()
    )

    st.write("Resumo anual")

    st.dataframe(
        resumo,
        hide_index=True
    )


# ==========================
# LAYOUT PRINCIPAL
# ==========================

col_esq, col_dir = st.columns([2, 1])

with col_esq:

    st.subheader(
        "Distribuição das taxas por ano"
    )

    fig_box = px.box(
        df_all,
        x="Year",
        y="Taxa",
        color="Year",
        points="all"
    )

    st.plotly_chart(
        fig_box,
        use_container_width=True
    )

    st.subheader(
        "Comparação dos municípios"
    )

    if sel_mun:

        df_sel = df_all[
            df_all["Municipio"]
            .isin(sel_mun)
        ]

        fig_line = px.line(
            df_sel,
            x="Year",
            y="Taxa",
            color="Municipio",
            markers=True
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

with col_dir:

    st.subheader(
        "Ranking por ano"
    )

    ano = st.selectbox(
        "Ano",
        sorted(
            df_all["Year"].unique(),
            reverse=True
        )
    )

    top_n = st.slider(
        "Top",
        5,
        30,
        10
    )

    ranking = (
        df_all[
            df_all["Year"] == ano
        ]
        .sort_values(
            "Taxa",
            ascending=False
        )
        .head(top_n)
    )

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )   


# ==========================
# MAPA REGIONAL DO BRASIL
# ==========================

REGIONAL_DF = load_region_abandono(REGIONAL_DATA_PATH)

st.subheader("Comparativo nacional por região")

if REGIONAL_DF.empty:
    st.warning(
        "Dados regionais não encontrados. Verifique o arquivo "
        f"{REGIONAL_DATA_PATH}"
    )
else:
    region_year = st.selectbox(
        "Ano para comparativo regional",
        sorted(REGIONAL_DF["Ano"].unique(), reverse=True),
        index=0
    )

    df_region_year = REGIONAL_DF[
        REGIONAL_DF["Ano"] == region_year
    ].copy()

    fig_region_bar = px.bar(
        df_region_year,
        x="Unidade_Geografica",
        y="Taxa_Abandono",
        color="Unidade_Geografica",
        text=df_region_year["Taxa_Abandono"].round(2),
        labels={
            "Unidade_Geografica": "Região",
            "Taxa_Abandono": "Taxa de Abandono (%)"
        }
    )
    fig_region_bar.update_layout(
        showlegend=False,
        xaxis_tickangle=-45,
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    st.plotly_chart(fig_region_bar, use_container_width=True)

    fig_region_line = px.line(
        REGIONAL_DF,
        x="Ano",
        y="Taxa_Abandono",
        color="Unidade_Geografica",
        markers=True,
        labels={
            "Ano": "Ano",
            "Taxa_Abandono": "Taxa de Abandono (%)",
            "Unidade_Geografica": "Região"
        }
    )
    st.plotly_chart(fig_region_line, use_container_width=True)

    if LOCAL_GEOJSON_PATH.exists() and LOCAL_IBGE_MUNICIPIOS_PATH.exists():
        try:
            df_ibge_all = pd.read_csv(
                LOCAL_IBGE_MUNICIPIOS_PATH,
                dtype=str,
                encoding='utf-8',
                engine='python'
            )
            df_ibge_all['Regiao'] = df_ibge_all['id'].str[:2].map(STATE_TO_REGION)
            df_ibge_all = df_ibge_all[
                df_ibge_all['Regiao'].notna()
            ].copy()
            region_rates = dict(
                zip(
                    df_region_year["Unidade_Geografica"],
                    df_region_year["Taxa_Abandono"]
                )
            )
            df_ibge_all["Taxa_Abandono"] = df_ibge_all["Regiao"].map(region_rates)

            geojson_region = None
            try:
                with open(LOCAL_GEOJSON_PATH, encoding='utf-8') as f:
                    geojson_region = json.load(f)
                for feat in geojson_region.get('features', []):
                    props = feat.setdefault('properties', {})
                    if 'codarea' in props:
                        props['codarea'] = str(props['codarea'])
            except Exception:
                geojson_region = None

            if geojson_region is not None and df_ibge_all['Taxa_Abandono'].notna().any():
                fig_region_map = px.choropleth(
                    df_ibge_all,
                    geojson=geojson_region,
                    locations='id',
                    color='Taxa_Abandono',
                    hover_name='Regiao',
                    hover_data=['Regiao'],
                    featureidkey='properties.codarea',
                    projection='mercator',
                    color_continuous_scale='OrRd',
                    labels={"Taxa_Abandono": "Taxa de Abandono (%)"}
                )
                fig_region_map.update_geos(fitbounds='locations', visible=False)
                fig_region_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig_region_map, use_container_width=True)
            else:
                st.info("Não foi possível gerar o mapa regional com os dados disponíveis.")
        except Exception as exc:
            st.warning(f"Erro ao gerar o mapa regional: {exc}")


map_year = st.selectbox(
    "Ano para mapa",
    sorted(df_all["Year"].unique(), reverse=True)
)

st.subheader(f"Mapa do Brasil - Top municípios por evasão ({map_year})")

map_top_n = st.slider("Top municípios no mapa", 5, 50, 20)

df_map = (
    df_all[df_all["Year"] == map_year]
    .sort_values("Taxa", ascending=False)
    .head(map_top_n)
    .copy()
)


def _normalize(name: str) -> str:
    if not isinstance(name, str):
        return ""
    s = name.strip().upper()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('Ã', 'A').replace('Á', 'A').replace('É', 'E')
    return s


df_map["_mun_norm"] = df_map["Municipio"].apply(_normalize)

geojson = None
if LOCAL_GEOJSON_PATH.exists():
    try:
        with open(LOCAL_GEOJSON_PATH, encoding='utf-8') as f:
            geojson = json.load(f)
        for feat in geojson.get('features', []):
            props = feat.setdefault('properties', {})
            if 'codarea' in props:
                props['codarea'] = str(props['codarea'])
    except Exception as e:
        st.warning(f"Erro ao carregar GeoJSON local: {e}")
else:
    st.warning(f"Arquivo GeoJSON local não encontrado: {LOCAL_GEOJSON_PATH}")

ibge_code_map = {}
if LOCAL_IBGE_MUNICIPIOS_PATH.exists():
    try:
        df_ibge = pd.read_csv(
            LOCAL_IBGE_MUNICIPIOS_PATH,
            dtype={"id": str},
            encoding='utf-8'
        )
        df_ibge['nome_norm'] = df_ibge['nome'].apply(_normalize)
        ibge_code_map = dict(zip(df_ibge['nome_norm'], df_ibge['id']))
    except Exception as e:
        st.warning(f"Erro ao ler a lista de municípios IBGE: {e}")
else:
    st.warning(f"Arquivo de códigos IBGE não encontrado: {LOCAL_IBGE_MUNICIPIOS_PATH}")

if motivos_df is not None:
    motivos_df.columns = [c.strip() for c in motivos_df.columns]

    motivos_map = motivos_df.copy()
    if 'Ano' in motivos_map.columns:
        motivos_map = motivos_map[motivos_map['Ano'] == map_year]
    if 'Year' in motivos_map.columns:
        motivos_map = motivos_map[motivos_map['Year'] == map_year]

    if 'Municipio' in motivos_map.columns and 'Motivo' in motivos_map.columns:
        motivos_map['municipio_norm'] = motivos_map['Municipio'].apply(_normalize)
        df_map = df_map.merge(
            motivos_map[['municipio_norm', 'Motivo']],
            left_on='_mun_norm',
            right_on='municipio_norm',
            how='left'
        )

df_map['ibge_id'] = df_map['_mun_norm'].map(ibge_code_map)
missing_ids = df_map[df_map['ibge_id'].isna()]
if not missing_ids.empty:
    st.info(
        "Não foi possível encontrar código IBGE para: "
        + ", ".join(sorted(missing_ids['Municipio'].unique()))
    )

if geojson is None or df_map['ibge_id'].notna().sum() == 0:
    st.info("Não há mapa disponível para o conjunto atual de municípios. Exibindo gráfico de barras.")
    df_display = df_map.copy()
    fig_bar = px.bar(
        df_display,
        x='Municipio',
        y='Taxa',
        color='Taxa',
        text=df_display['Taxa'].round(2)
    )
    fig_bar.update_layout(xaxis_tickangle=-45, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_bar, use_container_width='content')
    st.markdown("**Tabela dos top selecionados**")
    cols = ['Municipio', 'Taxa'] + (['Motivo'] if 'Motivo' in df_display.columns else [])
    st.dataframe(df_display[cols], use_container_width='content', hide_index=True)
else:
    df_map_geo = df_map.dropna(subset=['ibge_id']).copy()
    df_map_geo['ibge_id'] = df_map_geo['ibge_id'].astype(str)

    hover_data = ['Taxa']
    if 'Motivo' in df_map_geo.columns:
        hover_data.append('Motivo')

    try:
        fig_map = px.choropleth(
            df_map_geo,
            geojson=geojson,
            locations='ibge_id',
            color='Taxa',
            hover_name='Municipio',
            hover_data=hover_data,
            featureidkey='properties.codarea',
            projection='mercator',
            color_continuous_scale='OrRd'
        )
        fig_map.update_geos(fitbounds='locations', visible=False)
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width='content')
        st.markdown("**Tabela dos top selecionados**")
        st.dataframe(
            df_map[['Municipio', 'Taxa'] + (['Motivo'] if 'Motivo' in df_map.columns else [])],
            use_container_width='content',
            hide_index=True
        )
    except Exception as e:
        st.warning(f"Erro ao gerar o mapa: {e}")