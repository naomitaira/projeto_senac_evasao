import pandas as pd

# carregar arquivo
df = pd.read_csv(
    'censo_escolar_2024_senac.csv',
    sep=';',
    encoding='latin1',
    low_memory=False
)

# limpar nomes das colunas
df.columns = df.columns.str.strip().str.lower()

# verificar colunas (debug)
print(df.columns.tolist())

# selecionar colunas importantes
colunas_importantes = [
    'nu_ano_censo',
    'no_regiao',
    'sg_uf',
    'no_municipio',
    'no_entidade',
    'qt_mat_bas',
    'dt_ano_letivo_inicio'
]

df = df[colunas_importantes]

# converter número (matrículas)
df['qt_mat_bas'] = pd.to_numeric(df['qt_mat_bas'], errors='coerce')

# converter data
if 'dt_ano_letivo_inicio' in df.columns:
    df['dt_ano_letivo_inicio'] = pd.to_datetime(
        df['dt_ano_letivo_inicio'],
        format='%d%b%Y:%H:%M:%S',
        errors='coerce'
    )

# remover nulos
df = df.dropna()

# salvar CSV tratado
df.to_csv('censo_tratado.csv', sep=';', index=False)

# visualizar
print(df.head())
print(df.columns)