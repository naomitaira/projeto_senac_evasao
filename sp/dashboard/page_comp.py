import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

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
        "Top N",
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
# COMPARATIVO 2022 x 2024
# ==========================

st.subheader(
    "Variação entre 2022 e 2024"
)

comparativo = (
    df_all.pivot_table(
        index="Municipio",
        columns="Year",
        values="Taxa"
    )
)

if (
    2022 in comparativo.columns
    and 2024 in comparativo.columns
):

    comparativo["Diferença"] = (
        comparativo[2024]
        - comparativo[2022]
    )

    st.dataframe(
        comparativo.sort_values(
            "Diferença",
            ascending=False
        ),
        use_container_width=True
    )

# ==========================
# DOWNLOAD
# ==========================

st.subheader(
    "Exportar dados"
)

csv = df_all.to_csv(
    index=False,
    sep=";",
    decimal=","
)

st.download_button(
    "Baixar CSV consolidado",
    csv,
    file_name="abandono_2022_2024.csv",
    mime="text/csv"
)