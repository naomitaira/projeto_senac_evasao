import pandas as pd

arquivo = ['AbandonoEscolar_RendaMedia_2013_2023.csv',
           'censo_escolar_2025_senac.csv',
           'inep_indicadores_educacionais_brasil.csv',
           'Taxas_de_Rendimento_Escolar_2013_2023.csv']
for i in arquivo:
    df = pd.read_csv(i, encoding='latin1', sep=';')
    print(f"Dados do arquivo {i}:")
    print(df.head())
