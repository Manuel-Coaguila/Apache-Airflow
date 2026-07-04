from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime
import os
# from dotenv import load_dotenv

# # Cargar variables del .env
# load_dotenv()

with DAG(
    dag_id="INSERT_DATAFRAME_PRUEBA",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    ejecutar_script = DockerOperator(
        task_id="Insertar_dataframe_prueba",
        image="pipelines-test-python",
        command="python /opt/project/shared/py_003.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="tesis-net",
        mount_tmp_dir=False,
        mounts=[
            Mount(source="/home/mcoaguila/Escritorio/Proyecto_Tesis/pipelines/shared", target="/opt/project/shared", type="bind")
        ],
        auto_remove='force',
    )
    
    ejecutar_script
