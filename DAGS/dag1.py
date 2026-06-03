from airflow import DAG
from airflow.operators.python import PythonOperator

import sys


sys.path.append('/home/naomitaira/airflow/projeto_senac_evasao/sp/scripts/extracao_api_evasao')
from extrair_dados import carregar_dados
from transformar_dados import transformar_dados
from inep_indic_mysql import carga_inep_indicadores_mysql
from censo_escolar2024_2025 import carga_censo_escolar_mysql
from abandono_escolar_mysql import carga_indicadores_mysql
import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",           # seu usuário
        password="senac", # sua senha
        database="dados_educacao"
    )
    return conn


from datetime import datetime

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
        python_callable=carregar_dados
    )


    # tarefa para transformar os dados 
    task_transformar_dados = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar_dados
    )
    
    # tarefa para carregar os indicadores da INEP
    task_carregar_indicadores_inep = PythonOperator(
        task_id='carregar_indicadores_inep',  
        python_callable=carga_inep_indicadores_mysql
    )

    # tarefa para carregar o censo escolar

    task_carregar_censos = PythonOperator(
        task_id='carregar_censos_escolares',  
        python_callable=carga_censo_escolar_mysql
    )
    # tarefa para carregar os indicadores de abandono

    task_carregar_indicadores_abandono = PythonOperator(
        task_id='carregar_abandono_escolar',  
        python_callable=carga_indicadores_mysql
    )


    # definir a ordem das tarefas
    task_extrair_dados >> task_transformar_dados >> task_carregar_indicadores_inep >> task_carregar_censos >> task_carregar_indicadores_abandono
