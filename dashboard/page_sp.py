# Página de análise para São Paulo
import streamlit as st
import pandas as pd
from utils_dados import carregar_dados
import os 
import plotly.express as px
# Configurações de estilo para garantir legibilidade dos textos
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

# Definição das colunas de infraestrutura e seus rótulos amigáveis
 
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
# Rótulos mais amigáveis para exibição 
INFRA_LABELS = {
    'Acesso à internet para alunos':            'Internet',
    'Acesso ao Laboratório de informática':      'Lab. Informática',
    'Acesso à Biblioteca':                       'Biblioteca',
    'Acesso à Alimentação':                      'Alimentação',
    'Acesso ao Refeitório':                      'Refeitório',
    'Acesso à Água potável':                     'Água Potável',
    'Acesso à Energia elétrica da rede pública': 'Energia Elétrica',
    'Acesso à Esgoto da rede pública':           'Esgoto',
    'Acesso ao Banheiro':                        'Banheiro',
    'Acesso à Quadra de esportes':               'Quadra de Esportes',
}
# Carregamento dos dados com caching para otimizar performance 
@st.cache_data
def carregar_dados():
    abandono = {
        ano: pd.read_excel(f"sp/dados_limpos/total_abandono_escolar_{ano}_excel.xlsx")
        for ano in [2022, 2023, 2024]
    }
 
    frames = []
    for ano in [2022, 2023, 2024]:
        path = f"sp/dados_limpos/relacao_evasao_infraestrutura_{ano}.xlsx"
        if os.path.exists(path):
            df = pd.read_excel(path)
            df['Ano'] = ano
            df['Total Abandono Escolar'] = pd.to_numeric(df['Total Abandono Escolar'], errors='coerce')
            frames.append(df)
 
    return abandono, pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
 
abandono, df_all = carregar_dados()
 
# Estilo para garantir que os textos dos KPIs e títulos sejam legíveis, mesmo com temas escuros
 
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
# Título da página 
st.title("Evasão Escolar — São Paulo ✵")
# Subtítulo para contextualizar a análise
st.divider()
# Verificação se os dados foram carregados corretamente
if df_all.empty:
    st.warning("Arquivos não encontrados. Rode o script de processamento primeiro.")
    st.stop()
 
# Instruções para o usuário sobre como usar os filtros e interpretar os gráficos
 
st.text("Selecione o ano, número de municípios e infraestrutura para análise:")
# Filtros para seleção de ano, número de municípios e infraestrutura para análise
col_f1, col_f2, col_f3 = st.columns(3)
ano_sel   = col_f1.selectbox("Ano", sorted(df_all['Ano'].unique(), reverse=True))
n_top     = col_f2.selectbox("Top municípios", [5, 10, 15, 20], index=1)
infra_cor = col_f3.selectbox("Infraestrutura para scatter", COLUNAS_INFRA, format_func=lambda x: INFRA_LABELS[x])
 
st.divider()
# Filtragem dos dados para o ano selecionado e preparação para análise
df_ano = df_all[df_all['Ano'] == ano_sel].copy()
anos_disp = sorted(df_all['Ano'].unique())
 
# Cálculo dos KPIs principais: média de evasao.
 
media_atual = df_ano['Total Abandono Escolar'].mean()
delta = None
if ano_sel != anos_disp[0]:
    media_ant = df_all[df_all['Ano'] == anos_disp[anos_disp.index(ano_sel) - 1]]['Total Abandono Escolar'].mean()
    delta = media_atual - media_ant
 
pior_mun = df_ano.loc[df_ano['Total Abandono Escolar'].idxmax(), 'Municipio']
pior_val = df_ano['Total Abandono Escolar'].max()
 
# infra com menor acesso médio — aponta o recurso mais deficiente
media_infra = df_ano[COLUNAS_INFRA].mean()
pior_infra_col = media_infra.idxmin()
pior_infra_val = media_infra.min()
# Exibição dos KPIs principais em formato de métricas 
k1, k2, k3 = st.columns(3)
k1.metric("Taxa média de evasão", f"{media_atual:.2f}%", delta=f"{delta:+.2f}pp" if delta else None, delta_color="inverse")
k2.metric("Maior evasão", f"{pior_val:.1f}%", delta=pior_mun.title(), delta_color="off")
k3.metric("Infra mais deficiente", INFRA_LABELS[pior_infra_col], delta=f"{pior_infra_val:.1f}% de acesso médio", delta_color="off")
 
st.divider()
 
# ─── GRÁFICOS DE ANÁLISE ───
 
col_a, col_b = st.columns(2)
# Gráfico de barras para os municípios com maior evasão
with col_a:
    st.subheader(f"Top {n_top} municípios")
    top_n = df_ano.sort_values('Total Abandono Escolar', ascending=False).head(n_top)
    fig1 = px.bar(
        top_n[::-1], x='Total Abandono Escolar', y='Municipio', orientation='h',
        text='Total Abandono Escolar', color='Total Abandono Escolar',
        color_continuous_scale="blues",
        labels={'Total Abandono Escolar': 'Evasão (%)', 'Municipio': ''},
    )
    fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig1.update_layout(coloraxis_showscale=False, margin=dict(r=50))
    st.plotly_chart(fig1, use_container_width=True)
# Gráfico de linha para evolução da evasão ao longo dos anos 
with col_b:
    st.subheader("Evolução por ano")
    evolucao = df_all.groupby('Ano')['Total Abandono Escolar'].mean().reset_index()
    fig2 = px.line(
        evolucao, x='Ano', y='Total Abandono Escolar',
        markers=True, text='Total Abandono Escolar',
        labels={'Total Abandono Escolar': 'Evasão média (%)'},
    )
    fig2.update_traces(texttemplate='%{text:.2f}%', textposition='top center')
    fig2.update_layout(xaxis=dict(tickvals=[2022, 2023, 2024]))
    st.plotly_chart(fig2, use_container_width=True)
 
st.divider()

# Gráfico de barras horizontais para correlação entre evasão e infraestrutura
 
st.subheader("Correlação entre evasão e infraestrutura")
corrs = {
    INFRA_LABELS[col]: df_ano['Total Abandono Escolar'].corr(df_ano[col])
    for col in COLUNAS_INFRA if col in df_ano.columns
}
corr_df = pd.DataFrame(list(corrs.items()), columns=['Infraestrutura', 'Correlação']).sort_values('Correlação')
fig5 = px.bar(
    corr_df, x='Correlação', y='Infraestrutura', orientation='h',
    text='Correlação', color='Correlação',
    color_continuous_scale='blues', range_color=[-0.5, 0.5],
)
fig5.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig5.update_layout(coloraxis_showscale=False, margin=dict(r=60))
st.plotly_chart(fig5, use_container_width=True)
# Gráfico de calor para visualização da infraestrutura nos municípios com maior evasão
st.subheader("Infraestrutura — top municípios")
top15 = (
        df_ano.sort_values('Total Abandono Escolar', ascending=False)
        .head(15).set_index('Municipio')[COLUNAS_INFRA]
        .rename(columns=INFRA_LABELS)
    )
fig4 = px.imshow(top15, color_continuous_scale='blues', zmin=0, zmax=100, aspect='auto', labels=dict(color='%'))
fig4.update_layout(xaxis=dict(tickangle=-30))
st.plotly_chart(fig4, use_container_width=True)
 
st.divider()
 
