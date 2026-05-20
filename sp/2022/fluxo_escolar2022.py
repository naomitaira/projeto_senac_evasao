import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 2. CONFIGURAÇÃO VISUAL (opcional, deixa bonito)
sns.set_style("whitegrid")

# 3. CAMINHO DO ARQUIVO
base_dir = os.path.dirname(__file__)
arquivo = os.path.join(base_dir, 'Fluxo Escolar 2022 - por escola.csv')

# 4. LEITURA DOS DADOS
dados = pd.read_csv(arquivo, sep=';', encoding='latin1')

# 5. INSPEÇÃO DOS DADOS
print(dados.head())
print(dados.columns)

# 6. (OPCIONAL) FILTRAR PARA NÃO GERAR MUITOS GRÁFICOS
top_municipios = dados['NM_MUNICIPIO'].value_counts().head(2).index
dados_filtrado = dados[dados['NM_MUNICIPIO'].isin(top_municipios)]

# 7. GRÁFICO PRINCIPAL (estilo igual ao da imagem)
sns.set_style("whitegrid")

top_dir = dados['NM_DIRETORIA'].value_counts().head(4).index
dados_filtrado = dados[dados['NM_DIRETORIA'].isin(top_dir)]

sns.barplot(
    data=dados_filtrado,
    x="NM_DIRETORIA",
    y="APR_1",
    hue="CD_REDE_ENSINO"
)

plt.xticks(rotation=45)
plt.show()

# 8. GRÁFICO EXTRA (comparação)
sns.kdeplot(data=dados, x="APR_1", label="Aprovação")
sns.kdeplot(data=dados, x="REP_1", label="Reprovação")

plt.legend()
plt.show()
