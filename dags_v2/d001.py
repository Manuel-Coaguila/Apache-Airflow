from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime



# DAG que orquesta la ejecución del script de Python
with DAG(
    dag_id="dag_orquesta_pandas",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # ejecución manual
    catchup=False,
) as dag:

    ejecutar_script = BashOperator(
        task_id="ejecutar_pandas_demo",
        bash_command="python /opt/airflow/shared/001.py"
    )
