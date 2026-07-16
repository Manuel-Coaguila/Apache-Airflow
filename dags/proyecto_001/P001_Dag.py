from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

# Definir DAG
with DAG(
    dag_id="spark_sqlserver_dag",
    start_date=datetime(2026, 6, 19),
    schedule=None,   # ejecuta manualmente, puedes poner cron si quieres
    catchup=False,
) as dag:

    move_file_csv = BashOperator(
        task_id="move_file_csv",
        bash_command='''
            echo "######################################"
            echo "######################################"
            echo "INICIANDO VALIDACION DEL ARCHIVO .CSV"
            echo "######################################"
            echo "######################################"

            file_origen="/opt/airflow/nas/Proyecto_001/Employee.csv"
            file_destino="/opt/spark/projects/proyecto_001/files/input/Employee.csv"
            if [ -f "$file_origen" ]; then
                echo "ARHIVO .CSV ENCONTRADO"
                echo "COPIANDO ARCHIVO .CSV"
                cp "$file_origen" "$file_destino"
                echo "ARCHIVO COPIANDO EXITOSAMENTE .CSV"
            else
                echo "ARCHIVO NO ENCONTRADO"
                exit 1
            fi    
'''

    )
    # Tarea: ejecutar script con SparkSubmitOperator
    run_spark_job = SparkSubmitOperator(
        task_id="read_sqlserver_table",
        application="/opt/spark/projects/proyecto_001/main.py",   # ruta accesible por Spark
        conn_id="spark_default",
        jars="/opt/spark/jars/mssql-jdbc-12.6.3.jre8.jar",
        deploy_mode="client",   # clave: Spark ejecuta el .py
        verbose=True
    )

    task_end = BashOperator(
        task_id="task_end",
        bash_command='''
            echo "######################################"
            echo "######################################"
            echo "TAREA FINALIZADA"
            echo "######################################"
            echo "######################################"
'''
    )

    move_file_csv >> run_spark_job >> task_end
