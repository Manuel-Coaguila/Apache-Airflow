from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.task.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import random

def run_spark_job():
    print("⚡ Simulando ejecución de Spark job...")
    if random.choice([True, False]):
        raise Exception("❌ Error simulado en Spark job")
    print("✅ Spark job completado")

def notify_success():
    print("✅ Notificación simulada: Proceso completado correctamente")

def notify_failure():
    print("❌ Notificación simulada: Proceso fallido, revisar logs")

with DAG(
    dag_id="complex_spark_etl_simulation",
    start_date=datetime(2024, 1, 1),
    schedule=None,   # usa schedule_interval en lugar de schedule
    catchup=False,
    tags=["simulation", "spark", "etl"],
    default_args={
        "owner": "manuel",
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
        "email": ["manuelcoaguila2018@gmail.com"],   # notificación clásica opcional
        "email_on_failure": True,
        "email_on_retry": False,
    },
) as dag:

    start = PythonOperator(
        task_id="start_process",
        python_callable=lambda: print("🚀 Inicio"),
    )

    spark_job = PythonOperator(
        task_id="run_spark_job",
        python_callable=run_spark_job,
    )

    quality_check = BranchPythonOperator(
        task_id="check_quality",
        python_callable=lambda: "notify_success" if random.choice([True, False]) else "notify_failure",
    )

    notify_success_task = PythonOperator(
        task_id="notify_success",
        python_callable=notify_success,
    )

    notify_failure_task = PythonOperator(
        task_id="notify_failure",
        python_callable=notify_failure,
    )

    end = EmptyOperator(
        task_id="end",
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    start >> spark_job >> quality_check
    quality_check >> [notify_success_task, notify_failure_task] >> end
