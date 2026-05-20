import pandas as pd
import os


##################### TRATAR FLUXOS ESCOLARES #####################


# Carregar os arquivos CSV por escola e por município

df1 = pd.read_csv(r'sp\2022\Fluxo Escolar 2022 - por escola.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df2 = pd.read_csv(r'sp\2023\Fluxo Escolar 2023 - por escola.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df3 = pd.read_csv(r'sp\2024\Fluxo Escolar 2024 - por escola.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')

df4 = pd.read_csv(r'sp\2022\Fluxo Escolar 2022 - por municipio.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df5 = pd.read_csv(r'sp\2023\Fluxo Escolar 2023 - por municipio.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df6 = pd.read_csv(r'sp\2024\Fluxo Escolar 2024 - por municipio.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')

# Substituir os nomes das colunas para um formato mais amigável

renomear_colunas = {
    'NM_MUNICIPIO': 'Municipio',
    'NM_COMPLETO_ESCOLA': 'Escola',
    'ABA_1': 'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
    'ABA_2': 'Porcentagem de abandono - Ensino fundamental - Anos Finais',
    'ABA_3': 'Porcentagem de abandono - Ensino Médio',
}

df1 = df1.rename(columns=renomear_colunas)
df2 = df2.rename(columns=renomear_colunas)
df3 = df3.rename(columns=renomear_colunas)
df4 = df4.rename(columns=renomear_colunas)
df5 = df5.rename(columns=renomear_colunas)
df6 = df6.rename(columns=renomear_colunas)

# Mostrar apenas as colunas relevantes

# Para os arquivos por escola, manter as colunas de município, escola e as porcentagens de abandono

df1 = df1[['Municipio', 
        'Escola', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df2 = df2[['Municipio', 
        'Escola', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df3 = df3[['Municipio', 
        'Escola', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

#  Para os arquivos por município, manter as colunas de município e as porcentagens de abandono

df4 = df4[['Municipio', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df5 = df5[['Municipio', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df6 = df6[['Municipio', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]


# Limpar os dados, retirando linhas com valores faltantes ou inválidos

df1 = df1.dropna(axis=0, how='any')
df2 = df2.dropna(axis=0, how='any')
df3 = df3.dropna(axis=0, how='any')
df4 = df4.dropna(axis=0, how='any')
df5 = df5.dropna(axis=0, how='any')
df6 = df6.dropna(axis=0, how='any')

# Criar pasta de saída se não existir
os.makedirs(r'sp/dados_limpos', exist_ok=True)


# Salvar o resultado em um novo arquivo csv

df1.to_csv(r'sp/dados_limpos/fluxo_escolar_escola_2022_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df2.to_csv(r'sp/dados_limpos/fluxo_escolar_escola_2023_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df3.to_csv(r'sp/dados_limpos/fluxo_escolar_escola_2024_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df4.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2022_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df5.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2023_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df6.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2024_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')

print(f'Arquivos foram limpos e salvos')

##################### FIM DO TRATAMENTO DOS FLUXOS ESCOLARES #####################

