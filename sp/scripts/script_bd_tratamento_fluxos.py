import pandas as pd
import os


##################### TRATAR FLUXOS ESCOLARES #####################


# Carregar os arquivos CSV por município

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

df_fluxo_2022_municipio = df_fluxo_2022_municipio.rename(columns=renomear_colunas)
df_fluxo_2023_municipio = df_fluxo_2023_municipio.rename(columns=renomear_colunas)
df_fluxo_2024_municipio = df_fluxo_2024_municipio.rename(columns=renomear_colunas)

# Mostrar apenas as colunas relevantes

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

df_fluxo_2022_municipio = df_fluxo_2022_municipio.dropna(axis=0, how='any')
df_fluxo_2023_municipio = df_fluxo_2023_municipio.dropna(axis=0, how='any')
df_fluxo_2024_municipio = df_fluxo_2024_municipio.dropna(axis=0, how='any')

# Verificar quais são os municípios que possuem mais ou menos abandono escolar

# Calcular o total de abandono escolar por município para cada ano 

colunas_abandono = [
    'Porcentagem de abandono - Ensino fundamental - Anos Iniciais',
    'Porcentagem de abandono - Ensino fundamental - Anos Finais',
    'Porcentagem de abandono - Ensino Médio'
]


def calcular_total_abandono(df):

    # Converter valores para número
    for coluna in colunas_abandono:

        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(',', '.', regex=False)
        )

        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    # Somar os percentuais
    df['Total Abandono Escolar'] = df[colunas_abandono].sum(axis=1)

    # Agrupar por município
    total_abandono = (
        df.groupby('Municipio')['Total Abandono Escolar']
        .mean()
        .round(2)
        .sort_values(ascending=False)
    )

    return total_abandono


# Calcular abandono por ano

abandono_2022 = calcular_total_abandono(df_fluxo_2022_municipio)
abandono_2023 = calcular_total_abandono(df_fluxo_2023_municipio)
abandono_2024 = calcular_total_abandono(df_fluxo_2024_municipio)

# Criar pasta de saída se não existir
os.makedirs(r'sp/dados_limpos', exist_ok=True)


# Salvar os resultados em um novo arquivo csv

df_fluxo_2022_municipio.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2022_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2023_municipio.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2023_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df_fluxo_2024_municipio.to_csv(r'sp/dados_limpos/fluxo_escolar_municipio_2024_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')

# Salvar os percentuais de abandono por município em um novo arquivo csv

abandono_2022.to_csv(r'sp/dados_limpos/abandono_escolar_2022.csv',sep=';',decimal=',',encoding='utf-8')

abandono_2023.to_csv(r'sp/dados_limpos/abandono_escolar_2023.csv',sep=';',decimal=',',encoding='utf-8')

abandono_2024.to_csv(r'sp/dados_limpos/abandono_escolar_2024.csv',sep=';',decimal=',',encoding='utf-8')

print(f'Arquivos foram limpos e salvos')

##################### FIM DO TRATAMENTO DOS FLUXOS ESCOLARES #####################

