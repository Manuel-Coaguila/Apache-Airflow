FROM apache/airflow:3.2.2

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY spark-4.0.3-bin-hadoop3 /opt/spark
RUN rm -rf /opt/spark/R /opt/spark/data /opt/spark/examples /opt/spark/licenses
COPY extra_jars/*.jar /opt/spark/jars/

ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$SPARK_HOME/bin

USER airflow

RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark \
    apache-airflow-providers-microsoft-mssql \
    apache-airflow-providers-smtp \
    apache-airflow-providers-http \
    apache-airflow-providers-slack \
    apache-airflow-providers-openlineage \
    apache-airflow-providers-sftp

