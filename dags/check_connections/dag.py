from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime

def test_connection():
    conn = BaseHook.get_connection("spark_default")
    print("Host:", conn.host)
    print("Port:", conn.port)
    print("Login:", conn.login)
    print("Schema:", conn.schema)

with DAG(
    dag_id="check_connections",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["check", "connection"],
) as dag:

    check_spark = PythonOperator(
        task_id="check_spark_conn",
        python_callable=test_connection,
    )
