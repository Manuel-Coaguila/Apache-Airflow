from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="proyecto_001_dag",
    start_date=datetime(2026, 6, 19),
    schedule=None,
    catchup=False,
    tags=["proyecto_001", "spark", "csv"],
) as dag:

    move_file_csv = BashOperator(
        task_id="move_file_csv",
        bash_command="/opt/airflow/dags/proyecto_001/scripts/bash/move_csv.sh ",
        retries=2,
        retry_delay=timedelta(minutes=2),
        retry_exponential_backoff=True,
    )

    run_spark_job = SparkSubmitOperator(
        task_id="read_sqlserver_table",
        application="/opt/spark/projects/proyecto_001/main.py",
        conn_id="spark_default",
        jars="/opt/spark/jars/mssql-jdbc-12.6.3.jre8.jar",
        deploy_mode="client",
        verbose=False,
        execution_timeout=timedelta(hours=1),
    )

    task_end = BashOperator(
        task_id="task_end",
        bash_command='echo "TAREA FINALIZADA"',
    )

    move_file_csv >> run_spark_job >> task_end
