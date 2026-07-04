from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.task.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import random

def ejecutar_spark():
    print("⚡ Simulando Spark...")
    if random.choice([True, False]):
        raise Exception("❌ Error simulado en Spark")
    print("✅ Spark completado")

def validar_calidad():
    print("🔍 Validando calidad...")
    return random.choice([
        "rama_calidad_ok",
        "rama_calidad_error",
        "rama_datos_duplicados",
        "rama_esquema_invalido"
    ])

def auditar_datos():
    print("📑 Auditoría completada")

def actualizar_diccionario():
    print("📚 Diccionario actualizado")

def cargar_sqlserver():
    print("💾 Carga en SQL Server simulada")

def cargar_s3():
    print("☁️ Carga en S3/MinIO simulada")

def manejar_error():
    print("⚠️ Manejo de error de calidad")

def manejar_duplicados():
    print("⚠️ Manejo de datos duplicados")

def manejar_esquema():
    print("⚠️ Manejo de esquema inválido")

def notificar_exito():
    print("✅ Notificación de éxito")

def notificar_fallo():
    print("❌ Notificación de fallo")

with DAG(
    dag_id="etl_complejo_multiramas",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "spark", "auditoria", "diccionario", "ramas"],
    default_args={
        "owner": "manuel",
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:

    inicio = PythonOperator(
        task_id="inicio_proceso",
        python_callable=lambda: print("🚀 Inicio del proceso"),
    )

    spark = PythonOperator(
        task_id="ejecutar_spark",
        python_callable=ejecutar_spark,
    )

    validar = BranchPythonOperator(
        task_id="validar_calidad",
        python_callable=validar_calidad,
    )

    rama_calidad_ok = PythonOperator(
        task_id="rama_calidad_ok",
        python_callable=auditar_datos,
    )

    rama_calidad_error = PythonOperator(
        task_id="rama_calidad_error",
        python_callable=manejar_error,
    )

    rama_datos_duplicados = PythonOperator(
        task_id="rama_datos_duplicados",
        python_callable=manejar_duplicados,
    )

    rama_esquema_invalido = PythonOperator(
        task_id="rama_esquema_invalido",
        python_callable=manejar_esquema,
    )

    diccionario = PythonOperator(
        task_id="actualizar_diccionario",
        python_callable=actualizar_diccionario,
    )

    cargar_sql = PythonOperator(
        task_id="cargar_sqlserver",
        python_callable=cargar_sqlserver,
    )

    cargar_s3_task = PythonOperator(
        task_id="cargar_s3",
        python_callable=cargar_s3,
    )

    notificar_ok = PythonOperator(
        task_id="notificar_exito",
        python_callable=notificar_exito,
    )

    notificar_fail = PythonOperator(
        task_id="notificar_fallo",
        python_callable=notificar_fallo,
    )

    fin = EmptyOperator(
        task_id="fin",
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    # Flujo principal
    inicio >> spark >> validar
    validar >> rama_calidad_ok >> [diccionario, cargar_sql, cargar_s3_task] >> notificar_ok >> fin
    validar >> rama_calidad_error >> notificar_fail >> fin
    validar >> rama_datos_duplicados >> notificar_fail >> fin
    validar >> rama_esquema_invalido >> notificar_fail >> fin
