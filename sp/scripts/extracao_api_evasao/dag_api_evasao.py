from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
from sp.scripts.extracao_api_evasao import extrair_dados
from sp.scripts.extracao_api_evasao import transformar_dados
from sp.scripts.extracao_api_evasao import analisar_dados


# configuracoes da DAG


with DAG(
    'dag_api_evasao',
    description='DAG para extracao e transformacao de dados de evasao escolar',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['evasao', 'escolar', 'projeto_evasao']
) as dag:


    # tarefa para extrair dados dos censos e fluxos escolares
    task_extrair_dados = PythonOperator(
        task_id='extrair_dados',
        python_callable=extrair_dados
    )


    # tarefa para transformar os dados extraidos da API
    task_transformar_dados = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar_dados
    )

    task_analisar_dados = PythonOperator(
        task_id='analisar_dados',  
        python_callable=analisar_dados
    )

    # definir a ordem das tarefas
    task_extrair_dados >> task_transformar_dados >> task_analisar_dados


