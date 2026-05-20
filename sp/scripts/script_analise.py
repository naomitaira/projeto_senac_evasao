import pandas as pd

# Carregar arquivos já tratados

abandono_2022 = pd.read_csv(
    r'sp/dados_limpos/abandono_escolar_2022.csv',
    sep=';',
    decimal=',',
    encoding='utf-8'
)

infra_2022 = pd.read_csv(
    r'sp/dados_limpos/censo_escolar_2022_limpo.csv',
    sep=';',
    decimal=',',
    encoding='utf-8'
)


# Juntar as tabelas

relacao_2022 = pd.merge(
    abandono_2022,
    infra_2022,
    left_on='Municipio',
    right_on='Municipio',
    how='inner'
)


# Mostrar resultado

print(relacao_2022.head())


# Salvar

relacao_2022.to_csv(
    r'sp/dados_limpos/relacao_evasao_infraestrutura_2022.csv',
    index=False,
    encoding='utf-8'
)