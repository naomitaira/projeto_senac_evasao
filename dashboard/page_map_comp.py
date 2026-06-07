import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils_dados import carregar_dados

CURRENT_DIR = Path(__file__).resolve().parent
SP_DASHBOARD_DIR = Path(__file__).resolve().parents[2] / "sp" / "dashboard"

LOCAL_GEOJSON_PATH = CURRENT_DIR / "brazil_municipios.geojson"
if not LOCAL_GEOJSON_PATH.exists():
    LOCAL_GEOJSON_PATH = SP_DASHBOARD_DIR / "brazil_municipios.geojson"

DATA_DIR = Path(__file__).resolve().parents[2] / "dados_evasao"

FILES = {
    2022: DATA_DIR / "censo_escolar_brasil_2022.xlsx",
    2023: DATA_DIR / "censo_escolar_brasil_2023.xlsx",
    2024: DATA_DIR / "censo_escolar_brasil_2024.xlsx",
}

st.set_page_config(layout="wide")
st.title("Mapa comparativo — Censo Escolar (Brasil 2022-2024) 🗺")

st.markdown(
    """
    Esta página cria um mapa choropleth comparativo entre os anos de 2022, 2023 e 2024
    usando os arquivos `censo_escolar_brasil_YYYY.xlsx` da pasta `dados_evasao`.
    """
)


def detect_code_column(df: pd.DataFrame) -> str | None:
    candidates = [c for c in df.columns if re.search(r'cod|codigo|id', c, re.I) and re.search(r'mun|municip', c, re.I)]
    if candidates:
        return candidates[0]
    # fallback: any column with mostly numeric values and length >=6
    for c in df.columns:
        ser = df[c].astype(str).str.replace(r'\D', '', regex=True)
        if ser.str.len().median() >= 6 and ser.str.isnumeric().mean() > 0.6:
            return c
    return None


def clean_code_series(s: pd.Series) -> pd.Series:
    s2 = s.astype(str).str.replace(r'\D', '', regex=True)
    return s2.str.zfill(7)


def load_and_prepare(path: Path, year: int) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    # read a sample to detect columns
    try:
        sample = pd.read_excel(path, nrows=200)
    except Exception as e:
        st.warning(f"Erro lendo {path.name}: {e}")
        return pd.DataFrame()

    code_col = detect_code_column(sample)
    if code_col is None:
        st.error(f"Não foi possível detectar coluna de código IBGE em {path.name}.")
        return pd.DataFrame()

    # read full file but only necessary columns
    usecols = [code_col]
    # try to include numeric columns as candidates for metric
    for c in sample.select_dtypes(include=[np.number]).columns[:6]:
        if c not in usecols:
            usecols.append(c)

    df = pd.read_excel(path, usecols=usecols)

    df = df.rename(columns={code_col: 'cod_ibge'})
    df['cod_ibge'] = clean_code_series(df['cod_ibge'])

    # find numeric column to visualize (default: first numeric)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != 'cod_ibge']

    if not numeric_cols:
        st.error(f"Nenhuma coluna numérica detectada em {path.name} para visualização.")
        return pd.DataFrame()

    # take the first numeric column as default metric
    metric = numeric_cols[0]

    df = df[['cod_ibge', metric]].copy()
    df = df.dropna(subset=['cod_ibge'])
    df[metric] = pd.to_numeric(df[metric], errors='coerce')
    df = df.dropna(subset=[metric])
    df = df.groupby('cod_ibge', as_index=False)[metric].mean()
    df = df.rename(columns={metric: 'value'})
    df['Year'] = year
    return df


def main():
    if not LOCAL_GEOJSON_PATH.exists():
        st.error(f"GeoJSON de municípios não encontrado: {LOCAL_GEOJSON_PATH}")
        st.stop()

    dfs = []
    for year, path in FILES.items():
        if path.exists():
            d = load_and_prepare(path, year)
            if not d.empty:
                dfs.append(d)
        else:
            st.info(f"Arquivo ausente: {path.name}")

    if not dfs:
        st.error("Nenhum dado carregado. Verifique os arquivos em dados_evasao.")
        st.stop()

    df_all = pd.concat(dfs, ignore_index=True)

    # load geojson
    with open(LOCAL_GEOJSON_PATH, 'r', encoding='utf-8') as f:
        geo = json.load(f)

    # allow user controls
    agg = st.sidebar.selectbox('Agregação', ['mean', 'sum'], index=0)
    years = sorted(df_all['Year'].unique())
    sel_years = st.sidebar.multiselect('Anos para exibir (se vazio: todos)', years, default=years)

    if sel_years:
        df_plot = df_all[df_all['Year'].isin(sel_years)].copy()
    else:
        df_plot = df_all.copy()

    if agg == 'sum':
        df_plot = df_plot.groupby(['cod_ibge', 'Year'], as_index=False)['value'].sum()
    else:
        df_plot = df_plot.groupby(['cod_ibge', 'Year'], as_index=False)['value'].mean()

    # Plotly choropleth expects locations matching geojson properties; this geojson uses 'codarea'
    fig = px.choropleth(
        df_plot,
        geojson=geo,
        locations='cod_ibge',
        color='value',
        featureidkey='properties.codarea',
        animation_frame='Year',
        color_continuous_scale='OrRd',
        labels={'value': 'Valor'},
        title='Mapa comparativo por município'
    )

    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0,'t':30,'l':0,'b':0})

    st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()
