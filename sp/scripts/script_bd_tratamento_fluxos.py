import pandas as pd
import os


##################### TRATAR FLUXOS ESCOLARES #####################


# Carregar os arquivos CSV por escola e por município

df_fluxo_2022_escola = pd.read_csv(r'sp\2022\Fluxo Escolar 2022 - por escola.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df_fluxo_2023_escola = pd.read_csv(r'sp\2023\Fluxo Escolar 2023 - por escola.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df_fluxo_2024_escola = pd.read_csv(r'sp\2024\Fluxo Escolar 2024 - por escola.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')

df_fluxo_2022_municipio = pd.read_csv(r'sp\2022\Fluxo Escolar 2022 - por municipio.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df_fluxo_2023_municipio = pd.read_csv(r'sp\2023\Fluxo Escolar 2023 - por municipio.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')
df_fluxo_2024_municipio = pd.read_csv(r'sp\2024\Fluxo Escolar 2024 - por municipio.csv', sep=';', encoding='latin-1', on_bad_lines='skip', engine='python')

# Substituir os nomes das colunas para um formato mais amigável

renomear_colunas = {
    'NM_MUNICIPIO': 'Municipio',
    'NM_COMPLETO_ESCOLA': 'Escola',
    'ABA_1': 'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
    'ABA_2': 'Porcentagem de abandono - Ensino fundamental - Anos Finais',
    'ABA_3': 'Porcentagem de abandono - Ensino Médio',
}

df_fluxo_2022_escola = df_fluxo_2022_escola.rename(columns=renomear_colunas)
df_fluxo_2023_escola = df_fluxo_2023_escola.rename(columns=renomear_colunas)
df_fluxo_2024_escola = df_fluxo_2024_escola.rename(columns=renomear_colunas)
df_fluxo_2022_municipio = df_fluxo_2022_municipio.rename(columns=renomear_colunas)
df_fluxo_2023_municipio = df_fluxo_2023_municipio.rename(columns=renomear_colunas)
df_fluxo_2024_municipio = df_fluxo_2024_municipio.rename(columns=renomear_colunas)

# Mostrar apenas as colunas relevantes

# Para os arquivos por escola, manter as colunas de município, escola e as porcentagens de abandono

df_fluxo_2022_escola = df_fluxo_2022_escola[['Municipio', 
        'Escola', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df_fluxo_2023_escola = df_fluxo_2023_escola[['Municipio', 
        'Escola', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df_fluxo_2024_escola = df_fluxo_2024_escola[['Municipio', 
        'Escola', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

#  Para os arquivos por município, manter as colunas de município e as porcentagens de abandono

df_fluxo_2022_municipio = df_fluxo_2022_municipio[['Municipio', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais', 
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df_fluxo_2023_municipio = df_fluxo_2023_municipio[['Municipio', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]

df_fluxo_2024_municipio = df_fluxo_2024_municipio[['Municipio', 
        'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
        'Porcentagem de abandono - Ensino fundamental - Anos Finais',
        'Porcentagem de abandono - Ensino Médio']]


# Limpar os dados, retirando linhas com valores faltantes ou inválidos

df_fluxo_2022_escola = df_fluxo_2022_escola.dropna(axis=0, how='any')
df_fluxo_2023_escola = df_fluxo_2023_escola.dropna(axis=0, how='any')
df_fluxo_2024_escola = df_fluxo_2024_escola.dropna(axis=0, how='any')
df_fluxo_2022_municipio = df_fluxo_2022_municipio.dropna(axis=0, how='any')
df_fluxo_2023_municipio = df_fluxo_2023_municipio.dropna(axis=0, how='any')
df_fluxo_2024_municipio = df_fluxo_2024_municipio.dropna(axis=0, how='any')

# Criar pasta de saída se não existir
os.makedirs(r'sp/dados_limpos', exist_ok=True)


# Salvar o resultado em um novo arquivo csv

df_fluxo_2022_escola.to_csv(r'sp/dados_limpos/fluxo_escolar_escola_2022_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2023_escola.to_csv(r'sp/dados_limpos/fluxo_escolar_escola_2023_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2024_escola.to_csv(r'sp/dados_limpos/fluxo_escolar_escola_2024_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2022_municipio.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2022_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2023_municipio.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2023_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2024_municipio.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2024_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')

print(f'Arquivos foram limpos e salvos')

##################### FIM DO TRATAMENTO DOS FLUXOS ESCOLARES #####################

