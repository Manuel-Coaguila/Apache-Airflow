from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

# Definir DAG
with DAG(
    dag_id="spark_sqlserver_dag",
    start_date=datetime(2026, 6, 19),
    schedule=None,   # ejecuta manualmente, puedes poner cron si quieres
    catchup=False,
) as dag:

    # Tarea: ejecutar script con SparkSubmitOperator
    run_spark_job = SparkSubmitOperator(
        task_id="read_sqlserver_table",
        application="/opt/airflow/spark-jobs/002.py",   # ruta accesible por Spark
        conn_id="spark_default",
        jars="/opt/airflow/extra-jars/mssql-jdbc-13.4.0.jre11.jar",
        deploy_mode="client",   # clave: Spark ejecuta el .py
        verbose=True
    )

    run_spark_job
