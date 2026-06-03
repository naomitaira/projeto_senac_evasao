import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
import unicodedata

LOCAL_GEOJSON_PATH = Path(__file__).resolve().parent / "brazil_municipios.geojson"
LOCAL_IBGE_MUNICIPIOS_PATH = Path(__file__).resolve().parent / "ibge_municipios.csv"

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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Municípios",
        df_all["Municipio"].nunique()
    )

with col2:
    st.metric(
        "Taxa Média",
        f"{df_all['Taxa'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Maior Taxa",
        f"{df_all['Taxa'].max():.2f}%"
    )


# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.header("Filtros")

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

    # Opcional: upload de motivos (CSV com colunas Municipio;Motivo) => encontre uma maneira de fazer isso 
   

## ==========================
## MAPA BRASIL - TOP 20
## ==========================

st.subheader("Mapa do Brasil - Top municípios por evasão")

map_year = st.selectbox(
    "Ano para mapa",
    sorted(df_all["Year"].unique(), reverse=True)
)

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
    if 'Municipio' in motivos_df.columns and 'Motivo' in motivos_df.columns:
        motivos_df['municipio_norm'] = motivos_df['Municipio'].apply(_normalize)
        df_map = df_map.merge(
            motivos_df[['municipio_norm', 'Motivo']],
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
