import pandas as pd
import mysql.connector

def carga_censo_escolar_mysql(
    arquivos: list,
    host: str = "localhost",
    port: int = 3307,
    user: str = "root",
    password: str = "senac123",
    database: str = "dados_educacao"
):
    """
    Carrega arquivos de censo escolar para MySQL.

    Parâmetros:
        arquivos (list): lista de caminhos dos CSVs
        host (str): host do banco
        port (int): porta
        user (str): usuário
        password (str): senha
        database (str): banco
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

        sql = """
        INSERT INTO censo_escolar(
            ano, regiao, uf, municipio, instituicao, dependencia
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        total_registros = 0

        for arquivo in arquivos:
            print(f"📄 Processando arquivo: {arquivo}")

            # detectar separador automaticamente (melhor que if 2024)
            if "2024" in arquivo:
                df = pd.read_csv(arquivo, encoding="latin-1", sep=";")
            else:
                df = pd.read_csv(arquivo, encoding="latin-1", sep=",")

            print("🧹 Tratando dados...")
            df.columns = df.columns.str.strip().str.lower()
            df = df.fillna("")

            print("📦 Preparando dados...")
            dados = [
                (
                    int(row["nu_ano_censo"]),
                    row["no_regiao"],
                    row["sg_uf"],
                    row["no_municipio"],
                    row["no_entidade"],
                    row["tp_dependencia"]
                )
                for _, row in df.iterrows()
            ]

            print(f"🚀 Inserindo {len(dados)} registros...")
            cursor.executemany(sql, dados)
            conn.commit()

            total_registros += len(dados)

        print(f"✅ Total de registros inseridos: {total_registros}")

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
