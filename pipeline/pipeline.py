# importação de módulos e configuração do caminho para acessar os scripts de extração
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sp.scripts.extracao_api_evasao.censo_escolar2024_2025 import carga_censo_escolar_mysql
<<<<<<< HEAD
# from sp.scripts.extracao_api_evasao.inep_indic_mysql import carga_inep_indicadores_mysql
# from sp.scripts.extracao_api_evasao.abandono_escolar_mysql import carga_indicadores_mysql

=======
from sp.scripts.extracao_api_evasao.inep_indic_mysql import carga_inep_indicadores_mysql
from sp.scripts.extracao_api_evasao.abandono_escolar_mysql import carga_indicadores_mysql
# Função principal para executar a pipeline de carregamento dos dados
>>>>>>> 7b1bef464a25fd807d687cd241b8036f07ef4ebf
def executar_pipeline():
    print("🔹 Carga censo")
    # carga_censo_escolar_mysql([
    #     "dados_evasao/censo_escolar_2024_senac.csv",
    #     "dados_evasao/censo_escolar_2025_senac.csv"
    # ])

    carga_censo_escolar_mysql([
        "sp/dados_limpos/censo_escolar_2022_limpo.csv",
        "sp/dados_limpos/censo_escolar_2023_limpo.csv",
        "sp/dados_limpos/censo_escolar_2024_limpo.csv",
        "sp/dados_limpos/fluxo_escolar_municipio_2022_limpo.csv",
        "sp/dados_limpos/fluxo_escolar_municipio_2023_limpo.csv",
        "sp/dados_limpos/fluxo_escolar_municipio_2024_limpo.csv"
    ])

    # print("🔹 Carga indicadores")
    # # carga_indicadores_mysql(
    # #     "dados_evasao/AbandonoEscolar_RendaMedia_2013_2023.csv"
    # # )

<<<<<<< HEAD
    # carga_indicadores_mysql(
    #     "sp/dados_limpos/AbandonoEscolar_RendaMedia_2013_2023.csv"
    # )

    # print("🔹 Carga INEP")
    # carga_inep_indicadores_mysql(
    #    "dados_evasao/inep_indicadores_educacionais_brasil.csv"
    # )

=======
    print("🔹 Carga INEP")
    carga_inep_indicadores_mysql(
       "dados_evasao/inep_indicadores_educacionais_brasil.csv"
    )
# Execução da pipeline quando o script for executado diretamente
>>>>>>> 7b1bef464a25fd807d687cd241b8036f07ef4ebf
if __name__ == "__main__":
    executar_pipeline()