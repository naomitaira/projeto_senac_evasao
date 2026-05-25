import pandas as pd
import os


def carregar_dados():
    # ler arquivos csv com pandas
    print("Carregando dados do Censo Escolar 2022...")
    df_censo_2022  = pd.read_csv("sp/dados_limpos/censo_escolar_2022_limpo.csv", sep=";", encoding="latin-1")

    print("Carregando dados do Censo Escolar 2023...")
    df_censo_2023 = pd.read_csv("sp/dados_limpos/censo_escolar_2023_limpo.csv", sep=";", encoding="latin-1")

    print("Carregando dados do Censo Escolar 2024...")
    df_censo_2024 = pd.read_csv("sp/dados_limpos/censo_escolar_2024_limpo.csv", sep=";", encoding="latin-1")

    print("Carregando dados do Fluxo Escolar 2022...")
    df_fluxo_2022_municipio = pd.read_csv("sp/dados_limpos/fluxo_escolar_municipio_2022_limpo.csv", sep=";", encoding="latin-1")

    print("Carregando dados do Fluxo Escolar 2023...")
    df_fluxo_2023_municipio = pd.read_csv("sp/dados_limpos/fluxo_escolar_municipio_2023_limpo.csv", sep=";", encoding="latin-1")

    print("Carregando dados do Fluxo Escolar 2024...")
    df_fluxo_2024_municipio = pd.read_csv("sp/dados_limpos/fluxo_escolar_municipio_2024_limpo.csv", sep=";", encoding="latin-1")

    print('Dados extraídos com sucesso!')


if __name__ == "__main__":
    carregar_dados()

