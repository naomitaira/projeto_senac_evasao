import pandas as pd
import mysql.connector

# conexão com o banco
conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",       # coloque seu usuário
    password="senac",   # coloque sua senha
    database="dados_educacao"
)
cursor = conn.cursor()
# ler o CSV
df = pd.read_csv("banco_dados/dados/abandonoEscolar_RendaMedia_2013_2023.csv")
df.columns= df.columns.str.strip().str.lower()
df= df.fillna(0)
# tratar dados (evita erro)
df = df.fillna(0)
print(df.columns)
# inserir dados
sql = """
INSERT INTO indicadores_completo (
    ano, unidade_geografica, regiao, localizacao,
    dependencia_administrativa, grupo_de_abandono,
    taxa_abandono, renda_media
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

dados = []
renda_media= 0
for _, row in df.iterrows():
    dados.append((
        int(row["ano"]),
        row["unidade_geografica"],
        row["regiao"],
        row["localizacao"],
        row["dependencia_administrativa"],
        row["grupo_de_abandono"],
        float(row["taxa_abandono"]),
        float(row["renda_media"])
    ))

cursor.executemany(sql, dados)
conn.commit()
cursor.close()
conn.close()
print("✅ Dados inseridos com sucesso!")
