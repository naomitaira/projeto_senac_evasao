import pandas as pd
import os

##################### TRATAR CENSOS ESCOLARES #####################

# Carregar os arquivos CSV
df1 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2020_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df2 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2021_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df3 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2022_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df4 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2023_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df5 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2024_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df6 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2025_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')

# Deixar apenas as colunas relevantes 

colunas_relevantes = [
    'TP_DEPENDENCIA',
    'TP_LOCALIZACAO',
    'IN_INTERNET_ALUNOS',
    'QT_TABLET_ALUNO',
    'IN_LABORATORIO_INFORMATICA',
    'IN_BIBLIOTECA',
    'IN_ALIMENTACAO',
    'IN_REFEITORIO',
    'IN_AGUA_POTAVEL',
    'IN_ENERGIA_REDE_PUBLICA',
    'IN_ESGOTO_REDE_PUBLICA',
    'IN_BANHEIRO',
    'IN_QUADRA_ESPORTES'
]

# Selecionar as colunas relevantes e remover linhas com qualquer valor vazio

df_limpo1 = df1[colunas_relevantes].replace('', pd.NA).dropna(how='any')
df_limpo2 = df2[colunas_relevantes].replace('', pd.NA).dropna(how='any')
df_limpo3 = df3[colunas_relevantes].replace('', pd.NA).dropna(how='any')
df_limpo4 = df4[colunas_relevantes].replace('', pd.NA).dropna(how='any')
df_limpo5 = df5[colunas_relevantes].replace('', pd.NA).dropna(how='any')
df_limpo6 = df6[colunas_relevantes].replace('', pd.NA).dropna(how='any')


# Criar pasta de saída se não existir
os.makedirs('banco_dados/scripts/etl/bd/dados_limpos', exist_ok=True)

# Salvar o resultado em um novo arquivo 

df_limpo1.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2020_limpo.csv', index=False, encoding='utf-8')
df_limpo2.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2021_limpo.csv', index=False, encoding='utf-8')
df_limpo3.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2022_limpo.csv', index=False, encoding='utf-8')
df_limpo4.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2023_limpo.csv', index=False, encoding='utf-8')
df_limpo5.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2024_limpo.csv', index=False, encoding='utf-8')
df_limpo6.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2025_limpo.csv', index=False, encoding='utf-8')

print(f'Arquivos foram limpos e salvos')

# Checar se os arquivos foram salvos 

print('Processo concluído!')


##################### FIM DO TRATAMENTO DOS CENSOS ESCOLARES #####################