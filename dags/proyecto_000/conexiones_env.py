from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime

def test_connection():
    # Obtener la conexión por su conn_id
    conn = BaseHook.get_connection("spark_default")
    # Imprimir detalles en los logs de la tarea
    print("Host:", conn.host)
    print("Port:", conn.port)
    print("Login:", conn.login)
    print("Schema:", conn.schema)

with DAG(
    dag_id="check_connections",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    check_spark = PythonOperator(
        task_id="check_spark_conn",
        python_callable=test_connection,
    )
