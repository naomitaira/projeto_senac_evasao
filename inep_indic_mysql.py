import pandas as pd
import mysql.connector

def carga_inep_indicadores_mysql(
    caminho_csv: str,
    host: str = "localhost",
    port: int = 3307,
    user: str = "root",
    password: str = "senac",
    database: str = "dados_educacao"
):
    """
    Carrega indicadores educacionais do INEP para MySQL.

    Parâmetros:
        caminho_csv (str): caminho do arquivo CSV
        host (str): host do banco
        port (int): porta do banco
        user (str): usuário
        password (str): senha
        database (str): nome do banco
    """

    try:
        print("🔌 Conectando ao banco...")
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        print("📄 Lendo CSV...")
        df = pd.read_csv(caminho_csv, sep=";")

        print("🧹 Tratando dados...")
        df.columns = df.columns.str.strip().str.lower()
        df = df.fillna(0)

        print("📦 Preparando dados...")
        dados = [
            (
                int(row["ano"]),
                row["localizacao"],  # usado como região
                float(row["taxa_abandono_ef"]),
                0.0  # renda_media fixa
            )
            for _, row in df.iterrows()
        ]

        sql = """
        INSERT INTO indicadores_completos (
            ano, regiao, taxa_abandono, renda_media
        )
        VALUES (%s, %s, %s, %s)
        """

        print(f"🚀 Inserindo {len(dados)} registros...")
        cursor.executemany(sql, dados)
        conn.commit()

        print("✅ Dados inseridos com sucesso!")

    except Exception as e:
        print(f"❌ Erro na carga: {e}")
        raise

    finally:
        try:
            cursor.close()
            conn.close()
            print("🔒 Conexão encerrada.")
        except:
            pass
