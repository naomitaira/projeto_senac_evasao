Projeto: Evasão Escolar — Painel e Análises

Descrição

Projeto: Evasão Escolar — Painel e Análises

Descrição
- Aplicação Streamlit para comparar taxas de abandono escolar (2022–2024), gerar métricas e mapas.

Principais arquivos
- [dashboard/app_eva.py](dashboard/app_eva.py) — entrada / navegação das páginas do dashboard
- [dashboard/page_comp.py](dashboard/page_comp.py) — página de comparativo (métricas + mapa)
- [dashboard/page_sp.py](dashboard/page_sp.py) — página específica SP
- [dashboard/utils_dados.py](dashboard/utils_dados.py) — funções de carregamento de dados
- [pipeline/pipeline.py](pipeline/pipeline.py) — scripts de tratamento / pipeline (se aplicável)

Dados utilizados (local no repositório)
- [dados_evasao/AbandonoEscolar_RendaMedia_2013_2023.csv](dados_evasao/AbandonoEscolar_RendaMedia_2013_2023.csv)
- [dados_tratados/total_abandono_escolar_2022.csv](dados_tratados/total_abandono_escolar_2022.csv)
- [dados_tratados/total_abandono_escolar_2023.csv](dados_tratados/total_abandono_escolar_2023.csv)
- [dados_tratados/total_abandono_escolar_2024.csv](dados_tratados/total_abandono_escolar_2024.csv)
- (opcionais) motivos de evasão: [dados_tratados/motivos_evasao.csv](dados_tratados/motivos_evasao.csv)

GeoJSON / arquivos geoespaciais
- GeoJSON usado (fallback local): [sp/dashboard/br.json](sp/dashboard/br.json)
- Arquivo de municípios/IBGE usado para correspondência: [sp/dashboard/ibge_municipios.csv](sp/dashboard/ibge_municipios.csv)

Dependências
- Veja `requirements.txt` na raiz para a lista completa. Principais pacotes:
	- `streamlit`
	- `pandas`
	- `plotly`

Como rodar (Windows PowerShell)
```powershell
# ativar venv
& ".venv\Scripts\Activate.ps1"
# (opcional) limpar cache streamlit
streamlit cache clear
# configurar watcher por polling (recomendado em OneDrive)
$env:STREAMLIT_SERVER_FILE_WATCHER_TYPE='poll'
# rodar app
streamlit run dashboard/app_eva.py
```

Notas importantes
- Se os arquivos estiverem dentro do OneDrive, o hot-reload do Streamlit pode falhar; usar o watcher por polling (`STREAMLIT_SERVER_FILE_WATCHER_TYPE='poll'`) ou mover o projeto para uma pasta local (ex: `C:\dev\...`) melhora a atualização automática.
- O `page_comp.py` tenta três estratégias de mapeamento:
	1) usar `properties.codarea` no GeoJSON + `sp/dashboard/ibge_municipios.csv` para mapear por código IBGE municipal;
	2) usar `properties.id` com IDs `BRXX` para agregar por Unidade Federativa (UF);
	3) fallback por nome de município (pareamento tolerante após normalização).

Alterações realizadas durante a sessão
- `dashboard/page_comp.py`: refatorado e adicionado mapa (codarea / UF / fallback por nome).
- `dashboard/app_eva.py`: removido import de página que executava código no import time.

---

Resumo das alterações realizadas nesta sessão
-----------------------------------------
- Centralização do mapa para a região de São Paulo (controle via checkbox `foco_sp`).
- Filtragem para manter somente municípios do estado de São Paulo quando o arquivo `sp/dashboard/ibge_municipios.csv` estiver disponível.
- Métricas do mapa alteradas para priorizar indicadores de infraestrutura (média de acesso por tipo de infraestrutura; exibição da infraestrutura mais desenvolvida e da mais deficiente).
- Preferência pelo GeoJSON de São Paulo: `sp/dashboard/geojs-sao-paulo.json`.
- Implementação robusta de mapeamento entre dados e GeoJSON:
	1. Merge por código IBGE (`id`) usando `ibge_municipios.csv`.
	2. Fallback por nome de município com normalização (remoção de acentos, padronização de maiúsculas/espacos).
- Correções de bugs:
	- ` _normalize` movida para escopo global para evitar `NameError`.
	- `map_center` e `map_zoom` definidos para evitar `NameError` no plot.
	- Bloco de GeoJSON/plot substituído por rotina limpa e testável.

Arquivos relevantes
------------------
- `dashboard/page_mapa.py` — página do mapa (foco SP, métricas, merge com GeoJSON).
- `dashboard/utils_dados.py` — carregamento de dados e tratamento de infraestrutura.
- `sp/dashboard/geojs-sao-paulo.json` — GeoJSON municipal de São Paulo (usado quando presente).
- `sp/dashboard/ibge_municipios.csv` — CSV do IBGE para mapeamento por código.
- `sp/dados_limpos/relacao_evasao_infraestrutura_*.xlsx` — fontes de infraestrutura (2022–2024).

Tecnologias / linguagens utilizadas
----------------------------------
- Python — aplicação e análise (Streamlit, pandas, plotly.express).
- SQL — scripts em `banco_dados/` (dumps e queries auxiliares).
- JSON — GeoJSON para polígonos (`.json`).
- CSV / Excel — formatos de entrada (`.csv`, `.xlsx`).
- PowerShell / shell — comandos para ativar venv e rodar Streamlit no Windows.