import pandas as pd
import matplotlib.pyplot as plt


df_2025 = pd.read_csv('censo_escolar_2025_limpo.csv')
plt.figure(figsize=(10, 6))
plt.plot(df_2025['IN_ENERGIA_REDE_PUBLICA'], df_2025['IN_ESGOTO_REDE_PUBLICA'], label='2025')
plt.title('total de alunos 2025')
plt.xlabel('Energia - Rede Pública')
plt.ylabel('Esgoto - Rede Pública')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()