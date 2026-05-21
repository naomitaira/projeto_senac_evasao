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
df = pd.read_csv("banco_dados/dados/inep_indicadores_educacionais_brasil.csv",sep=";")
df.columns= df.columns.str.strip().str.lower()
df= df.fillna(0)
# tratar dados (evita erro)
df = df.fillna(0)
print(df.columns)
# inserir dados
sql = """
INSERT INTO indicadores (ano, regiao, taxa_abandono, renda_media)
VALUES (%s, %s, %s, %s)
"""
dados = []
renda_media= 0
for _, row in df.iterrows():
    dados.append((
        int(row["ano"]),
        row["localizacao"],
        float(row["taxa_abandono_ef"]),
        renda_media
    ))
cursor.executemany(sql, dados)
conn.commit()
cursor.close()
conn.close()
print("✅ Dados inseridos com sucesso!")
