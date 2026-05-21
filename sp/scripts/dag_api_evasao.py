from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import requests
from extracao_api_fruityvice.extrair_dados import extrair_dados
from extracao_api_fruityvice.transformar_dados import transformar_dados


# configuracoes da DAG


with DAG(
    'dag_api_fruityvice',
    description='DAG para extracao e transformacao de dados da API Fruityvice',
    schedule='*/10 * * * *',
    start_date=datetime(2026, 4, 7),
    catchup=False,
    tags=['fruityvice', 'projeto_api', 'api_fruityvice']
) as dag:


    # tarefa para extrair dados da API Fruityvice
    task_extrair_dados = PythonOperator(
        task_id='extrair_dados',
        python_callable=extrair_dados
    )


    # tarefa para transformar os dados extraidos da API Fruityvice
    task_transformar_dados = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar_dados
    )


    # definir a ordem das tarefas
    task_extrair_dados >> task_transformar_dados


