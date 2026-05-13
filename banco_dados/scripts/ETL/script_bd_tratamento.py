import pandas as pd

# Carregar o arquivo Excel
df = pd.read_excel('arquivo.xlsx')

# 1. Remover linhas onde TODAS as células estão em branco
df_limpo = df.dropna(how='all')

# 2. Remover linhas onde PELO MENOS UMA célula está em branco
# df_limpo = df.dropna(how='any')

# Salvar o resultado em um novo arquivo
df_limpo.to_excel('arquivo_limpo.xlsx', index=False)
