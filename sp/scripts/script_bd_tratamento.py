import pandas as pd
import os


##################### TRATAR FLUXOS ESCOLARES #####################


# Carregar os arquivos CSV

df1 = pd.read_csv('bd/2022/Fluxo Escolar 2022 - por escola.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df2= pd.read_csv('bd/2023/Fluxo Escolar 2023 - por escola.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df3 = pd.read_csv('bd/2024/Fluxo Escolar 2024 - por escola.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')

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

# Mostrar apenas as colunas relevantes

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

# Limpar os dados, retirando linhas com valores faltantes ou inválidos

df1 = df1.dropna(axis=0, how='any')
df2 = df2.dropna(axis=0, how='any')
df3 = df3.dropna(axis=0, how='any')

# Criar pasta de saída se não existir
os.makedirs('bd/dados_limpos', exist_ok=True)


# Salvar o resultado em um novo arquivo
# Usar separador ';' e decimal ',' para facilitar abertura no Excel PT-BR

df1.to_csv('bd/dados_limpos/fluxo_escolar_municipio_2022_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df2.to_csv('bd/dados_limpos/fluxo_escolar_municipio_2023_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')
df3.to_csv('bd/dados_limpos/fluxo_escolar_municipio_2024_limpo.csv', sep=';', decimal=',', index=False, encoding='utf-8')

print(f'Arquivos foram limpos e salvos')


# Checar se os arquivos foram salvos

print('Processo concluído!')


##################### FIM DO TRATAMENTO DOS FLUXOS ESCOLARES #####################

