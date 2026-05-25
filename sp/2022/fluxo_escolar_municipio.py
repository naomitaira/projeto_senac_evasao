import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lê o CSV com separador correto
dados = pd.read_csv(
    r"C:\Users\junio\OneDrive\Área de Trabalho\projeto_senac_evasao\sp\2022\Fluxo Escolar 2022 - por municipio.csv",
    encoding="utf-8-sig",
    sep=";"
)
# REMOVE caracteres invisíveis (BOM) e espaços
dados.columns = dados.columns.str.strip().str.replace("\ufeff", "", regex=True)

print("Colunas carregadas:", dados.columns.tolist())

# Converte vírgula para ponto
colunas_numericas = [
    "APR_1","REP_1","ABA_1",
    "APR_2","REP_2","ABA_2",
    "APR_3","REP_3","ABA_3"
]

for col in colunas_numericas:
    dados[col] = dados[col].astype(str).str.replace(",", ".")
    dados[col] = pd.to_numeric(dados[col], errors="coerce")

# Gráfico
sns.kdeplot(data=dados, x="APR_1", label="Aprovação 1º ciclo")
plt.legend()
plt.show()
