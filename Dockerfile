FROM apache/airflow:3.2.2

USER root

# 1. Instalación de dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openjdk-17-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar Spark dentro del contenedor
COPY spark-4.0.3-bin-hadoop3 /opt/spark

ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$SPARK_HOME/bin

# # 2. Crear usuario propio para Airflow con UID=1000 y GID=0 (root)
# ARG UID=1000
# ARG GID=0
# ARG AIRFLOW_USER=uairflow

# RUN useradd -m -u ${UID} -g ${GID} ${AIRFLOW_USER}

# # 3. Cambiar al nuevo usuario
# USER ${AIRFLOW_USER}

USER airflow

# 4. Instalación de paquetes de Python
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark \
    apache-airflow-providers-microsoft-mssql \
    apache-airflow-providers-smtp \
    apache-airflow-providers-http \
    apache-airflow-providers-slack \
    apache-airflow-providers-openlineage \
    apache-airflow-providers-sftp
