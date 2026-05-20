import pandas as pd


##################### CARREGAR ARQUIVOS #####################


# Evasão escolar por município

abandono_2022 = pd.read_csv(
    r'sp/dados_limpos/abandono_escolar_2022.csv',
    sep=';',
    encoding='utf-8'
)


# Infraestrutura por município

infra_2022 = pd.read_csv(
    r'sp/dados_limpos/censo_escolar_2022_limpo.csv',
    sep=',',
    encoding='utf-8'
)


##################### PADRONIZAR MUNICÍPIOS #####################


abandono_2022['Municipio'] = (
    abandono_2022['Municipio']
    .astype(str)
    .str.strip()
    .str.upper()
)

infra_2022['Municipio'] = (
    infra_2022['Municipio']
    .astype(str)
    .str.strip()
    .str.upper()
)


##################### JUNTAR AS TABELAS #####################


relacao_2022 = pd.merge(
    abandono_2022,
    infra_2022,
    on='Municipio',
    how='inner'
)

##################### MOSTRAR RESULTADOS #####################


print('\nQuantidade de linhas encontradas:')
print(relacao_2022.shape)


print('\nPrimeiras linhas:')
print(relacao_2022.head())


##################### SALVAR CSV FINAL #####################


relacao_2022.to_csv(
    r'sp/dados_limpos/relacao_evasao_infraestrutura_2022.csv',
    sep=',',
    decimal=',',
    index=False,
    encoding='utf-8'
)


print('\nArquivo salvo com sucesso!')