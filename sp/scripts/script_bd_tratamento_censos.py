import pandas as pd
import os
import csv


##################### TRATAR CENSOS ESCOLARES #####################

print("Carregando Censo 2022... (Isso pode levar um tempinho)")
df_censo_2022 = pd.read_csv(r'sp\2022\microdados_ed_basica_2022.csv', sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)


print("Carregando Censo 2023...")
df_censo_2023 = pd.read_csv(r'sp\2023\microdados_ed_basica_2023.csv', sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)


print("Carregando Censo 2024...")
df_censo_2024 = pd.read_csv(r'sp\2024\microdados_ed_basica_2024.csv', sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)

# Colunas que realmente precisamos (ajuda o pandas a carregar mais rápido se filtrarmos depois)


def renomear_colunas(df):

    renomear_colunas = {
        'NO_REGIAO': 'Região',
        'NO_UF': 'UF',
        'NO_MUNICIPIO': 'Municipio',
        'IN_INTERNET_ALUNOS': 'Acesso à internet para alunos',
        'QT_TABLET_ALUNO': 'Quantidade de tablets para alunos',
        'IN_LABORATORIO_INFORMATICA': 'Acesso ao Laboratório de informática',
        'IN_BIBLIOTECA': 'Acesso à Biblioteca',
        'IN_ALIMENTACAO': 'Acesso à Alimentação',
        'IN_REFEITORIO': 'Acesso ao Refeitório',
        'IN_AGUA_POTAVEL': 'Acesso à Água potável',
        'IN_ENERGIA_REDE_PUBLICA': 'Acesso à Energia elétrica da rede pública',
        'IN_ESGOTO_REDE_PUBLICA': 'Acesso à Esgoto da rede pública',
        'IN_BANHEIRO': 'Acesso ao Banheiro',
        'IN_QUADRA_ESPORTES': 'Acesso à Quadra de esportes'
    }

    return df.rename(columns=renomear_colunas)

df_censo_2022 = renomear_colunas(df_censo_2022)
df_censo_2023 = renomear_colunas(df_censo_2023)
df_censo_2024 = renomear_colunas(df_censo_2024)

colunas_relevantes = [
    'Região',
    'UF',
    'Municipio',
    'Acesso à internet para alunos',
    'Quantidade de tablets para alunos',
    'Acesso ao Laboratório de informática',
    'Acesso à Biblioteca',
    'Acesso à Alimentação',
    'Acesso ao Refeitório',
    'Acesso à Água potável',
    'Acesso à Energia elétrica da rede pública',
    'Acesso à Esgoto da rede pública',
    'Acesso ao Banheiro',
    'Acesso à Quadra de esportes'
]

colunas_percentuais = [
    'Acesso à internet para alunos',
    'Acesso ao Laboratório de informática',
    'Acesso à Biblioteca',
    'Acesso à Alimentação',
    'Acesso ao Refeitório',
    'Acesso à Água potável',
    'Acesso à Energia elétrica da rede pública',
    'Acesso à Esgoto da rede pública',
    'Acesso ao Banheiro',
    'Acesso à Quadra de esportes'
]



# Selecionar as colunas relevantes e remover linhas com qualquer valor vazio
def selecionar_colunas_existentes(df, colunas):
    colunas_existentes = [col for col in colunas if col in df.columns]
    return df[colunas_existentes].replace('', pd.NA).dropna(how='any').copy() # .copy() evita avisos de SettingWithCopyWarning


df_limpo1 = selecionar_colunas_existentes(df_censo_2022, colunas_relevantes)
df_limpo2 = selecionar_colunas_existentes(df_censo_2023, colunas_relevantes)
df_limpo3 = selecionar_colunas_existentes(df_censo_2024, colunas_relevantes)


# ##################### CALCULAR PERCENTUAIS DE INFRAESTRUTURA POR MUNICÍPIO #####################


colunas_percentuais = [
    'Acesso à internet para alunos',
    'Acesso ao Laboratório de informática',
    'Acesso à Biblioteca',
    'Acesso à Alimentação',
    'Acesso ao Refeitório',
    'Acesso à Água potável',
    'Acesso à Energia elétrica da rede pública',
    'Acesso à Esgoto da rede pública',
    'Acesso ao Banheiro',
    'Acesso à Quadra de esportes'
]
def calcular_percentuais_infraestrutura(df):

    infraestrutura = (
        df.groupby('Municipio')[colunas_percentuais]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )

    return infraestrutura

infra_2022 = calcular_percentuais_infraestrutura(df_limpo1)
infra_2023 = calcular_percentuais_infraestrutura(df_limpo2)
infra_2024 = calcular_percentuais_infraestrutura(df_limpo3)

# Criar pasta de saída se não existir

os.makedirs(r'sp/dados_limpos', exist_ok=True)

# Criar os arquivos de percentuais por município para cada ano

# 2022
                
with open(r'sp/dados_limpos/percentuais_infraestrutura_por_municipio_2022.csv',
          'w',
          newline='',
          encoding='utf-8') as f:

    f.write('Município,Percentual\n')

    infra_2022.to_csv(f, header=False, index=False)
    
# 2023
    
with open(r'sp/dados_limpos/percentuais_infraestrutura_por_municipio_2023.csv',
          'w',
          newline='',
          encoding='utf-8') as f:
    
    f.write('Município,Percentual\n')
    
    infra_2023.to_csv(f, header=False, index=False)
    
# 2024
    
with open(r'sp/dados_limpos/percentuais_infraestrutura_por_municipio_2024.csv',
          'w',
          newline='',
          encoding='utf-8') as f:
    
    f.write('Município,Percentual\n')
        
    infra_2024.to_csv(f, header=False, index=False)


colunas_booleanas = [
    'Acesso à internet para alunos',
    'Acesso ao Laboratório de informática',
    'Acesso à Biblioteca',
    'Acesso à Alimentação',
    'Acesso ao Refeitório',
    'Acesso à Água potável',
    'Acesso à Energia elétrica da rede pública',
    'Acesso à Esgoto da rede pública',
    'Acesso ao Banheiro',
    'Acesso à Quadra de esportes'
]


mapeamento_para_sim_nao = {
    1.0: 'Sim',
    0.0: 'Não',
    1: 'Sim',
    0: 'Não'
}


# Aplicando a substituição apenas nas colunas booleanas de infraestrutura
df_limpo1[colunas_booleanas] = df_limpo1[colunas_booleanas].replace(mapeamento_para_sim_nao)
df_limpo2[colunas_booleanas] = df_limpo2[colunas_booleanas].replace(mapeamento_para_sim_nao)
df_limpo3[colunas_booleanas] = df_limpo3[colunas_booleanas].replace(mapeamento_para_sim_nao)


# Salvar o resultado em um novo arquivo
print("Salvando os arquivos limpos...")
df_limpo1.to_csv(r'sp/dados_limpos/censo_escolar_2022_limpo.csv', index=False, encoding='utf-8')
df_limpo2.to_csv(r'sp/dados_limpos/censo_escolar_2023_limpo.csv', index=False, encoding='utf-8')
df_limpo3.to_csv(r'sp/dados_limpos/censo_escolar_2024_limpo.csv', index=False, encoding='utf-8')


print('Arquivos foram limpos e salvos com sucesso!')