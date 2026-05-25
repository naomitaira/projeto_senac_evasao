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
sql = """
insert into censo_escolar(
ano,regiao,uf,municipio,instituicao,dependencia
)values(%s,%s,%s,%s,%s,%s)
"""

arquivos = [
    "banco_dados/dados/censo_escolar_2024_senac.csv",
    "banco_dados/dados/censo_escolar_2025_senac.csv"
]
for arquivo in arquivos:

    # ✅ detectar separador
    if "2024" in arquivo:
        df = pd.read_csv(arquivo, encoding="latin-1", sep=";")
    else:
        df = pd.read_csv(arquivo, encoding="latin-1", sep=",")

    df.columns = df.columns.str.strip().str.lower()

    print(df.columns)  # ✅ para conferir

    df = df.fillna("")

    dados = []

    for _, row in df.iterrows():
        dados.append((
            int(row["nu_ano_censo"]),
            row["no_regiao"],
            row["sg_uf"],
            row["no_municipio"],
            row["no_entidade"],
            row["tp_dependencia"]
        ))

    cursor.executemany(sql, dados)
    conn.commit()
cursor.close()
conn.close()
print("Dados inseridos com sucesso!")