import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from utils_dados import carregar_dados
import unicodedata
import re

st.set_page_config(layout="wide")
st.title("Comparativo de Evasão Escolar (2022-2024) 📈")

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[1]

LOCAL_GEOJSON_PATH = CURRENT_DIR / "brazil_municipios.geojson"
LOCAL_IBGE_MUNICIPIOS_PATH = CURRENT_DIR / "ibge_municipios.csv"
# procurar alternativas
if not LOCAL_GEOJSON_PATH.exists():
    for alt in ("brazil_municipios.geojson", "brazil-municipalities.geojson", "br.json"):
        p = ROOT_DIR / "sp" / "dashboard" / alt
        if p.exists():
            LOCAL_GEOJSON_PATH = p
            break
if not LOCAL_IBGE_MUNICIPIOS_PATH.exists():
    p = ROOT_DIR / "sp" / "dashboard" / "ibge_municipios.csv"
    if p.exists():
        LOCAL_IBGE_MUNICIPIOS_PATH = p

motivos_df = None

# ------------------ funções de leitura ------------------
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

# ------------------ carregar dados ------------------
DATA_DIR = ROOT_DIR / "dados_tratados"
df_all = load_all(DATA_DIR)
if df_all.empty:
    st.error(f"Nenhum dado encontrado em {DATA_DIR}")
    st.stop()

# dados de infraestrutura (mantém separação)
BASE_DIR = "sp/dados_limpos"
abandono, df_infra = None, carregar_dados(BASE_DIR)

with st.sidebar:
    st.header("Filtros")
    ano_metricas = st.selectbox("Ano das métricas", sorted(df_all["Year"].unique(), reverse=True))
    municipios = sorted(df_all["Municipio"].unique())
    default_sel = (df_all.groupby("Municipio")["Taxa"].mean().sort_values(ascending=False).head(8).index.tolist())
    sel_mun = st.multiselect("Selecione municípios", municipios, default=default_sel)
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

# ------------------ métricas ------------------
df_metrics = df_all[df_all["Year"] == ano_metricas]
col1, col2, col3 = st.columns(3)
col1.metric("Municípios", df_metrics["Municipio"].nunique())
col2.metric("Taxa Média", f"{df_metrics['Taxa'].mean():.2f}%")
col3.metric("Maior Taxa", f"{df_metrics['Taxa'].max():.2f}%")
st.caption(f"Métricas calculadas para o ano {ano_metricas}.")

# ------------------ mapa simples (compacto) ------------------
def _normalize(s: str) -> str:
    if not isinstance(s, str):
        return ''
    s = s.upper()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Z0-9 ]+", ' ', s)
    return re.sub(r"\s+", ' ', s).strip()


def _load_geo(p: Path):
    try:
        if p.exists():
            return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None
    return None

geojson = _load_geo(LOCAL_GEOJSON_PATH) or _load_geo(ROOT_DIR / 'sp' / 'dashboard' / 'br.json')
if not geojson:
    st.info('GeoJSON não encontrado — mapa desabilitado.')
else:
    feats = geojson.get('features', [])
    if not feats:
        st.info('GeoJSON vazio — mapa desabilitado.')
    else:
        df_sel = df_all[df_all['Year'] == ano_metricas].copy()
        props = feats[0].get('properties', {})
        # 1) codarea (código IBGE municipal)
        if 'codarea' in props and LOCAL_IBGE_MUNICIPIOS_PATH.exists():
            df_ibge = pd.read_csv(LOCAL_IBGE_MUNICIPIOS_PATH, dtype={'id': str})
            df_ibge['nome_norm'] = df_ibge['nome'].map(_normalize)
            df_sel['Municipio_norm'] = df_sel['Municipio'].map(_normalize)
            merged = pd.merge(df_sel, df_ibge[['id', 'nome_norm']], left_on='Municipio_norm', right_on='nome_norm', how='left')
            merged = merged.dropna(subset=['id'])
            if merged.empty:
                st.info('Nenhum município mapeado via codarea.')
            else:
                df_map = merged.groupby('id')['Taxa'].mean().reset_index()
                df_map['id'] = df_map['id'].astype(str)
                fig = px.choropleth_mapbox(df_map, geojson=geojson, locations='id', featureidkey='properties.codarea',
                                           color='Taxa', color_continuous_scale='Reds', mapbox_style='carto-positron',
                                           zoom=4, center={'lat': -15.0, 'lon': -52.0}, opacity=0.7,
                                           labels={'Taxa': 'Taxa de Abandono (%)'})
                fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
                st.subheader('Mapa — Taxa média de abandono (por município)')
                st.plotly_chart(fig, use_container_width=True)
        # 2) id por estado (BRXX)
        elif any((f.get('properties', {}).get('id', '') or '').startswith('BR') for f in feats) and LOCAL_IBGE_MUNICIPIOS_PATH.exists():
            df_ibge = pd.read_csv(LOCAL_IBGE_MUNICIPIOS_PATH, dtype={'id': str})
            df_ibge['uf'] = df_ibge['id'].astype(str).str[:2]
            df_ibge['nome_norm'] = df_ibge['nome'].map(_normalize)
            df_sel['Municipio_norm'] = df_sel['Municipio'].map(_normalize)
            merged = pd.merge(df_sel, df_ibge[['id','uf','nome_norm']], left_on='Municipio_norm', right_on='nome_norm', how='left')
            merged = merged.dropna(subset=['uf'])
            if merged.empty:
                st.info('Nenhum município mapeado por UF.')
            else:
                uf_map = {
                    '11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA','22':'PI','23':'CE','24':'RN',
                    '25':'PB','26':'PE','27':'AL','28':'SE','29':'BA','31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS',
                    '50':'MS','51':'MT','52':'GO','53':'DF'
                }
                merged['uf_abbr'] = merged['uf'].map(uf_map)
                df_state = merged.groupby('uf_abbr')['Taxa'].mean().reset_index().dropna()
                if df_state.empty:
                    st.info('Nenhum estado mapeado.')
                else:
                    df_state['geo_id'] = 'BR' + df_state['uf_abbr']
                    fig = px.choropleth_mapbox(df_state, geojson=geojson, locations='geo_id', featureidkey='properties.id',
                                               color='Taxa', color_continuous_scale='Reds', mapbox_style='carto-positron',
                                               zoom=4, center={'lat': -15.0, 'lon': -52.0}, opacity=0.7,
                                               labels={'Taxa': 'Taxa de Abandono (%)'})
                    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
                    st.subheader('Mapa — Taxa média de abandono (por UF)')
                    st.plotly_chart(fig, use_container_width=True)
        # 3) fallback por nome
        else:
            prop_key = next((k for k in props.keys() if any(w in k.lower() for w in ('mun','nome','name','municip'))), None)
            if not prop_key:
                st.info("GeoJSON não tem chave de nome reconhecida nem codarea; mapa limitado.")
            else:
                df_map = df_sel.groupby('Municipio')['Taxa'].mean().reset_index()
                name_map = {f['properties'][prop_key].strip().lower(): f['properties'][prop_key] for f in feats if f.get('properties') and f['properties'].get(prop_key)}
                df_map['loc'] = df_map['Municipio'].astype(str).str.strip().str.lower().map(name_map)
                df_map = df_map.dropna(subset=['loc'])
                if df_map.empty:
                    st.info('Nenhum município compatível para plotar por nome.')
                else:
                    fig = px.choropleth_mapbox(df_map, geojson=geojson, locations='loc', featureidkey=f'properties.{prop_key}',
                                               color='Taxa', color_continuous_scale='Reds', mapbox_style='carto-positron',
                                               zoom=4, center={'lat': -15.0, 'lon': -52.0}, opacity=0.7,
                                               labels={'Taxa': 'Taxa de Abandono (%)'})
                    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
                    st.subheader('Mapa — Taxa média de abandono (por município)')
                    st.plotly_chart(fig, use_container_width=True)
