from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

with DAG(
    dag_id="SQL_SERVER",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    ejecutar_script = DockerOperator(
        task_id="ejecutar_pandas_demo",
        image="pipelines-test-python",
        command="python /opt/project/shared/py_002.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="tesis-net",
        mount_tmp_dir=False,
        mounts=[
            Mount(source="/home/mcoaguila/Escritorio/Proyecto_Tesis/pipelines/shared", target="/opt/project/shared", type="bind")
        ],
        environment={
            "SQL_SERVER_PASSWORD": os.getenv("SQL_SERVER_PASSWORD"),
            "SQL_SERVER_HOST": os.getenv("SQL_SERVER_HOST"),
            "SQL_SERVER_PORT": os.getenv("SQL_SERVER_PORT"),
            "SQL_SERVER_USER": os.getenv("SQL_SERVER_USER"),
            "SQL_SERVER_DATABASE": os.getenv("SQL_SERVER_DATABASE"),
        },
        auto_remove='force',
    )
    
    ejecutar_script
