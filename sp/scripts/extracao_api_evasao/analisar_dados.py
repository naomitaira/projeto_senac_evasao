import mysql.connector

def conectar_mysql():

    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="senac",
        database="dados_educacao"
    )

    return conn

def ler_csv(caminho, sep=",", encoding="utf-8"):

    df = pd.read_csv(
        caminho,
        sep=sep,
        encoding=encoding
    )

    df.columns = df.columns.str.strip().str.lower()

    return df.fillna(0)

def carregar_indicadores():

    conn = conectar_mysql()
    cursor = conn.cursor()

    df = ler_csv(
        "banco_dados/dados/inep_indicadores_educacionais_brasil.csv",
        sep=";"
    )

    sql = """
    INSERT INTO indicadores
    (ano, regiao, taxa_abandono, renda_media)
    VALUES (%s, %s, %s, %s)
    """

    dados = []

    for _, row in df.iterrows():

        dados.append((
            int(row["ano"]),
            row["localizacao"],
            float(row["taxa_abandono_ef"]),
            0
        ))

    cursor.executemany(sql, dados)

    conn.commit()

    cursor.close()
    conn.close()

    print("Indicadores carregados")
    
def carregar_censo():

    conn = conectar_mysql()
    cursor = conn.cursor()

    sql = """
    INSERT INTO censo_escolar(
        ano, regiao, uf,
        municipio, instituicao,
        dependencia
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    arquivos = [
        "banco_dados/dados/censo_escolar_2024_senac.csv",
        "banco_dados/dados/censo_escolar_2025_senac.csv"
    ]

    for arquivo in arquivos:

        if "2024" in arquivo:

            df = ler_csv(
                arquivo,
                sep=";",
                encoding="latin-1"
            )

        else:

            df = ler_csv(
                arquivo,
                sep=",",
                encoding="latin-1"
            )

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

    print("Censo carregado")
    
def carregar_indicadores_completo():

    conn = conectar_mysql()
    cursor = conn.cursor()

    df = ler_csv(
        "banco_dados/dados/abandonoEscolar_RendaMedia_2013_2023.csv"
    )

    sql = """
    INSERT INTO indicadores_completo (
        ano,
        unidade_geografica,
        regiao,
        localizacao,
        dependencia_administrativa,
        grupo_de_abandono,
        taxa_abandono,
        renda_media
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    dados = []

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

    print("Indicadores completos carregados")
    
if __name__ == "__main__":

    carregar_indicadores()
    carregar_censo()
    carregar_indicadores_completo()