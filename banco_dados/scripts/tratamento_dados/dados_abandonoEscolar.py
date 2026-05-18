import pandas as pd

df = pd.read_csv('AbandonoEscolar_RendaMedia_2013_2023.csv', encoding='utf-8', sep=',')
df.columns = df.columns.str.strip().str.lower()
print(df.head())

df.columns = df.columns.str.lower()
df = df.dropna(subset=['taxa_abandono'])
df.columns = df.columns.str.strip().str.lower()
df = df.dropna(subset=['taxa_abandono'])
df['ano'] = df['ano'].astype(int)
df['taxa_abandono'] = pd.to_numeric(df['taxa_abandono'], errors='coerce')
df['renda_media'] = pd.to_numeric(df['renda_media'], errors='coerce')
df_filtrado = df[
    (df['unidade_geografica'] == 'Brasil') &
    (df['localizacao'] == 'Total') &
    (df['dependencia_administrativa'] == 'Total')
]
print(df.columns.tolist())
df.to_csv('dados_abandono_escolar_filtrado.csv', index=False, encoding='utf-8')
print("✅ CSV tratado criado com sucesso!")