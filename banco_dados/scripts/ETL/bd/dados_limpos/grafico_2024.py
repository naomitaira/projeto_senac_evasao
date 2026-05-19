import pandas as pd
import matplotlib.pyplot as plt

df_2024 = pd.read_csv('censo_escolar_2024_limpo.csv')
plt.figure(figsize=(10, 6))
plt.plot(df_2024['IN_ENERGIA_REDE_PUBLICA'], df_2024['IN_ESGOTO_REDE_PUBLICA'], label='2024')
plt.title('total de alunos 2024')
plt.xlabel('Energia - Rede Pública')
plt.ylabel('Esgoto - Rede Pública')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

