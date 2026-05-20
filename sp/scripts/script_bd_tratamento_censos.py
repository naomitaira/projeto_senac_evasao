import pandas as pd
import os

##################### TRATAR CENSOS ESCOLARES #####################

# Carregar os arquivos CSV
df1 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2024_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')
df2 = pd.read_csv('banco_dados/scripts/etl/bd/censo_escolar_2025_senac.csv', sep=";", encoding='latin-1', on_bad_lines='skip', engine='python')

# Deixar apenas as colunas relevantes 

colunas_relevantes = [
    'NO_REGIAO', 
    'NO_UF',
    'NO_MUNICIPIO',
    'NO_ENTIDADE',
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

# Substituir 0/1 por Não/Sim nas colunas booleanas

colunas_booleanas = [
    'IN_INTERNET_ALUNOS',
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

mapeamento_para_sim_nao = {
    1.0: 'Sim',
    0.0: 'Não'
}

df_limpo1[colunas_booleanas] = df_limpo1[colunas_booleanas].replace(mapeamento_para_sim_nao)
df_limpo2[colunas_booleanas] = df_limpo2[colunas_booleanas].replace(mapeamento_para_sim_nao)

# Criar pasta de saída se não existir
os.makedirs('banco_dados/scripts/etl/dados_limpos', exist_ok=True)

# Salvar o resultado em um novo arquivo 

df_limpo1.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2024_limpo.csv', mode='w', index=False, encoding='utf-8')
df_limpo2.to_csv('banco_dados/scripts/etl/bd/dados_limpos/censo_escolar_2025_limpo.csv', mode='w', index=False, encoding='utf-8')


print(f'Arquivos foram limpos e salvos')

# Checar se os arquivos foram salvos 

print('Processo concluído!')




##################### FIM DO TRATAMENTO DOS CENSOS ESCOLARES #####################