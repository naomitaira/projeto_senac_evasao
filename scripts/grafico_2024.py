import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

base_dir = Path(__file__).resolve().parent
file_path = base_dir.parent / 'banco_dados' / 'dados_limpos' / 'censo_escolar_2024.csv'
df_2024 = pd.read_csv(file_path)
df_heat = df_2024.groupby(['IN_ENERGIA_REDE_PUBLICA', 'IN_ESGOTO_REDE_PUBLICA']).size().unstack(fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(df_heat, annot=True, fmt='d', cmap='blues')
plt.title('Relação entre Energia e Esgoto - 2024')
plt.xlabel('Esgoto - Rede Pública')
plt.ylabel('Energia - Rede Pública')
plt.xticks([0.5, 1.5], ['Não', 'Sim'])
plt.yticks([0.5, 1.5], ['Não', 'Sim'], rotation=0)
plt.tight_layout()
plt.show()
print(file_path)