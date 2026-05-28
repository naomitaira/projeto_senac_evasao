import pandas as pd
import mysql.connector

def carga_indicadores_mysql(
    caminho_csv: str,
    host: str = "localhost",
    port: int = 3307,
    user: str = "root",
    password: str = "senac123",
    database: str = "dados_educacao"
):
    """
    Função para carregar dados de abandono escolar + renda média para MySQL.

    Parâmetros:
        caminho_csv (str): caminho do arquivo CSV
        host (str): host do banco
        port (int): porta do banco
        user (str): usuário
        password (str): senha
        database (str): nome do banco
    """

    try:
        print("🔌 Conectando ao banco de dados...")
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        print("📄 Lendo CSV...")
        df = pd.read_csv(caminho_csv)

        print("🧹 Tratando dados...")
        df.columns = df.columns.str.strip().str.lower()
        df = df.fillna(0)

        sql = """
        INSERT INTO indicadores_completo (
            ano, unidade_geografica, regiao, localizacao,
            dependencia_administrativa, grupo_de_abandono,
            taxa_abandono, renda_media
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        print("📦 Preparando dados para inserção...")
        dados = [
            (
                int(row["ano"]),
                row["unidade_geografica"],
                row["regiao"],
                row["localizacao"],
                row["dependencia_administrativa"],
                row["grupo_de_abandono"],
                float(row["taxa_abandono"]),
                float(row["renda_media"])
            )
            for _, row in df.iterrows()
        ]

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