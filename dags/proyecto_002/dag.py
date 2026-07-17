from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="proyecto_002_dag",
    start_date=datetime(2026, 7, 16),
    schedule=None,
    catchup=False,
    tags=["proyecto_002"],
) as dag:
    pass
