from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from censo_escolar2024_2025 import carga_censo_escolar_mysql
from inep_indic_mysql import carga_inep_indicadores_mysql
from utils.carga_censo import carga_censo_escolar_mysql


with DAG(
    dag_id="pipeline_educacao",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    tarefa_censo = PythonOperator(
        task_id="carga_censo_mysql",
        python_callable=carga_censo_escolar_mysql,
        op_kwargs={
            "arquivos": [
                "/opt/airflow/dags/banco_dados/dados/censo_escolar_2024_senac.csv",
                "/opt/airflow/dags/banco_dados/dados/censo_escolar_2025_senac.csv"
            ]
        }
    )

    tarefa_indicadores = PythonOperator(
        task_id="carga_indicadores_mysql",
        python_callable=carga_indicadores_mysql,
        op_kwargs={
            "caminho_csv": "/opt/airflow/dags/banco_dados/dados/abandonoEscolar_RendaMedia_2013_2023.csv"
        }
    )

    tarefa_inep = PythonOperator(
        task_id="carga_inep_mysql",
        python_callable=carga_inep_indicadores_mysql,
        op_kwargs={
            "caminho_csv": "/opt/airflow/dags/banco_dados/dados/inep_indicadores_educacionais_brasil.csv"
        }
    )

    # ✅ Agora funciona
    tarefa_censo >> tarefa_indicadores >> tarefa_inep
