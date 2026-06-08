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

Próximos passos sugeridos
- Melhorar heurísticas de normalização de nomes (remoção de sufixos, abreviações) caso muitos municípios fiquem sem correspondência.
- Remover mensagens de debug do `page_comp.py` quando estiver satisfeito com o mapa.