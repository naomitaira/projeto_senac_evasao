from sp.scripts.extracao_api_evasao.censo_escolar2024_2025 import carga_censo_escolar_mysql
from sp.scripts.extracao_api_evasao.inep_indic_mysql import carga_inep_indicadores_mysql
from sp.scripts.extracao_api_evasao.abandono_escolar_mysql import carga_indicadores_mysql

def executar_pipeline():
    print("🔹 Carga censo")
    carga_censo_escolar_mysql([
        "C:/Users/Napoleao51241156/OneDrive - SENAC DF/Documentos/projeto_senac_evasao/banco_dados/dados/censo_escolar_2024_senac.csv",
        "C:/Users/Napoleao51241156/OneDrive - SENAC DF/Documentos/projeto_senac_evasao/banco_dados/dados/censo_escolar_2025_senac.csv"
    ])

    print("🔹 Carga indicadores")
    carga_indicadores_mysql(
        "C:/Users/Napoleao51241156/OneDrive - SENAC DF/Documentos/projeto_senac_evasao/banco_dados/dados/abandonoEscolar_RendaMedia_2013_2023.csv"
    )

    print("🔹 Carga INEP")
    carga_inep_indicadores_mysql(
        "C:/Users/Napoleao51241156/OneDrive - SENAC DF/Documentos/projeto_senac_evasao/banco_dados/dados/inep_indicadores_educacionais_brasil.csv"
    )

if __name__ == "__main__":
    executar_pipeline()