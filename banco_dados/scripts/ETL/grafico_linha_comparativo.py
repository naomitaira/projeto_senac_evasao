import pandas as pd
import matplotlib.pyplot as plt

df_2024 = pd.read_csv('censo_escolar_2024_limpo.csv')
df_2025 = pd.read_csv('censo_escolar_2025_limpo.csv')
plt.figure(figsize=(10, 6))
plt.plot(df_2024['NO_MUNICIPIO'], df_2024['QT_TABLET_ALUNO'], label='2024')


plt.title('total de alunos 2024')
plt.xlabel('Município')
plt.ylabel('Total de Alunos')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()