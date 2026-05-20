import pandas as pd
import os
import csv


##################### TRATAR CENSOS ESCOLARES #####################


# Colunas que realmente precisamos (ajuda o pandas a carregar mais rápido se filtrarmos depois)
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


print("Carregando Censo 2022... (Isso pode levar um tempinho)")
df_censo_2022 = pd.read_csv(r'sp\2022\microdados_ed_basica_2022.csv', sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)


print("Carregando Censo 2023...")
df_censo_2023 = pd.read_csv(r'sp\2023\microdados_ed_basica_2023.csv', sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)


print("Carregando Censo 2024...")
df_censo_2024 = pd.read_csv(r'sp\2024\microdados_ed_basica_2024.csv', sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)


# Selecionar as colunas relevantes e remover linhas com qualquer valor vazio
def selecionar_colunas_existentes(df, colunas):
    colunas_existentes = [col for col in colunas if col in df.columns]
    return df[colunas_existentes].replace('', pd.NA).dropna(how='any').copy() # .copy() evita avisos de SettingWithCopyWarning


df_limpo1 = selecionar_colunas_existentes(df_censo_2022, colunas_relevantes)
df_limpo2 = selecionar_colunas_existentes(df_censo_2023, colunas_relevantes)
df_limpo3 = selecionar_colunas_existentes(df_censo_2024, colunas_relevantes)


# ##################### CALCULAR PERCENTUAIS DE INFRAESTRUTURA POR MUNICÍPIO #####################


colunas_percentuais = [
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


df_combinado = pd.concat([df_limpo1, df_limpo2, df_limpo3], ignore_index=True)

with open(r'sp/dados_limpos/percentuais_infraestrutura_por_municipio.csv', 'w', newline='', encoding='utf-8') as f:

    for coluna in colunas_percentuais:
        if coluna in df_combinado.columns:
            coluna_nome = coluna.replace('IN_', '').replace('QT_', '').replace('_', ' ')
            percentuais = (
                df_combinado.groupby('NO_MUNICIPIO')[coluna]
                .mean()
                .mul(100)
                .round(1)
                .sort_values(ascending=False)
            )

            f.write(f'\nPercentual de escolas com {coluna_nome}:\n')
            percentuais.to_csv(f, header=True)


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
    0.0: 'Não',
    1: 'Sim',
    0: 'Não'
}


# Aplicando a substituição apenas nas colunas booleanas de infraestrutura
df_limpo1[colunas_booleanas] = df_limpo1[colunas_booleanas].replace(mapeamento_para_sim_nao)
df_limpo2[colunas_booleanas] = df_limpo2[colunas_booleanas].replace(mapeamento_para_sim_nao)
df_limpo3[colunas_booleanas] = df_limpo3[colunas_booleanas].replace(mapeamento_para_sim_nao)


# Criar pasta de saída se não existir
os.makedirs(r'sp/dados_limpos', exist_ok=True)


# Salvar o resultado em um novo arquivo
print("Salvando os arquivos limpos...")
df_limpo1.to_csv(r'sp/dados_limpos/censo_escolar_2022_limpo.csv', index=False, encoding='utf-8')
df_limpo2.to_csv(r'sp/dados_limpos/censo_escolar_2023_limpo.csv', index=False, encoding='utf-8')
df_limpo3.to_csv(r'sp/dados_limpos/censo_escolar_2024_limpo.csv', index=False, encoding='utf-8')


print('Arquivos foram limpos e salvos com sucesso!')