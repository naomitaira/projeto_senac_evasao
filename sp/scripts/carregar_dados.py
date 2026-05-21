import pandas as pd
from sqlalchemy import create_engine


def carregar_dados():
    # ler arquivo parquet
    df = pd.read_parquet("/home/naomitaira/datalake/bronze/frutas_transformadas.parquet")


    # criar conexao com o banco de dados usando o SQALAlchemy
    engine = create_engine("mysql+pymysql://fruityvice:senac@10.12.110.22:3307/db_fruityvice")


    # carregar dados no banco de dados mysql
    df.to_sql("fruits", con=engine, if_exists='replace', index=False)


    print("Número de registros carregados: ", len(df))


    print(df.head())


    print("Dados carregados no banco de dados com sucesso!")




if __name__ == "__main__":
    carregar_dados()
