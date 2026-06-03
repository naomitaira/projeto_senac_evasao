import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sp.scripts.extracao_api_evasao.censo_escolar2024_2025 import carga_censo_escolar_mysql
from sp.scripts.extracao_api_evasao.inep_indic_mysql import carga_inep_indicadores_mysql
from sp.scripts.extracao_api_evasao.abandono_escolar_mysql import carga_indicadores_mysql

def executar_pipeline():
    print("🔹 Carga censo")
    carga_censo_escolar_mysql([
        "dados_evasao/censo_escolar_2024_senac.csv",
        "dados_evasao/censo_escolar_2025_senac.csv"
    ])

    print("🔹 Carga indicadores")
    carga_indicadores_mysql(
        "dados_evasao/AbandonoEscolar_RendaMedia_2013_2023.csv"
    )

    print("🔹 Carga INEP")
    carga_inep_indicadores_mysql(
       "dados_evasao/inep_indicadores_educacionais_brasil.csv"
    )

if __name__ == "__main__":
    executar_pipeline()