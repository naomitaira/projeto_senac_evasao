# script para transformar os dados extraídos da API Fruityvice
# filtra dados apenas as frutas com menos de 50 calorias 
# realiza a tradução dos nomes das colunas para português usando a api LibreTranslate

# filtra todas as frutas com menos de 50 calorias

import pandas as pd
import os

try:
    import extracao_api_fruityvice.translator_api as translator
    import extracao_api_fruityvice.pesquisa_termos_wikipedia as pesquisa_termos_wikipedia
except ModuleNotFoundError:
    # Permite executar o script diretamente com python3 dags/extracao_api_fruityvice/transformar_dados.py
    # sem depender de um package instalado ou do PYTHONPATH.
    from pathlib import Path
    import sys

    package_dir = Path(__file__).resolve().parent
    if str(package_dir) not in sys.path:
        sys.path.insert(0, str(package_dir))

    import translator_api as translator
    import pesquisa_termos_wikipedia as pesquisa_termos_wikipedia


def filtrar_dados(df):
    return df[df['nutritions.calories'] <= 50]


def transformar_dados():
    #ler arquivo parquet
    df = pd.read_parquet('/home/naomitaira/datalake/raw/frutas.parquet')

    #filtrar dados
    df_filtrado = filtrar_dados(df)

    #traduzir dados
    translator_instance = translator.Translator()
    df_traduzido = traduzir_dados(df_filtrado,  translator_instance) 

    #inserir imagem
    df_traduzido = inserir_imagem(df_traduzido)

    # inserir coluna com dados da wikipedia
    df_traduzido['wikipedia'] = df_traduzido['name'].apply(lambda x: pesquisa_termos_wikipedia.buscar_wikipedia(x))
    print("Dados da Wikipedia inseridos com sucesso!")

    #salvar arquivo parquet
    df_traduzido.to_parquet('/home/naomitaira/datalake/bronze/frutas_transformadas.parquet', index=False)

    print("Dados transformados e salvos com sucesso!")

if __name__ == "__main__":
    transformar_dados()
