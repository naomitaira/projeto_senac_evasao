import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Estilo bonito
sns.set_theme(style="whitegrid")

df_escolar = pd.read_csv('dados_abandono_escolar_filtrado.csv')


# Normalizar nomes das colunas
df_escolar.columns = df_escolar.columns.str.lower()


plt.figure(figsize=(12, 6))

sns.lineplot(x=df_escolar['grupo_de_abandono'], y=df_escolar['renda_media'], label='renda_media', marker='o')

plt.xticks(rotation=90)
plt.title("Comparação de Abandono Escolar por Grupo", fontsize=16)
plt.xlabel("Grupo de Abandono")
plt.ylabel("Renda Média")
plt.tight_layout()
plt.show()
