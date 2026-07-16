# ============================================================
# DOCKERFILE NUEVO (optimizado)
# ============================================================

# STAGE 1: Generar JRE mínimo con jlink
# Usamos eclipse-temurin:17-jdk-alpine solo para ejecutar jlink
# y recortar el JRE a los módulos que Spark realmente necesita.
# Esto reduce de ~217 MB (openjdk-17-jre-headless) a ~90 MB.
FROM eclipse-temurin:17-jdk-alpine AS jre-builder
RUN jlink \
    --add-modules java.base,java.compiler,java.instrument,java.logging,java.management,\
java.naming,java.net.http,java.prefs,java.rmi,java.scripting,java.security.jgss,\
java.security.sasl,java.sql,java.sql.rowset,java.transaction.xa,java.xml,java.xml.crypto,\
jdk.httpserver,jdk.management,jdk.management.agent,jdk.naming.dns,jdk.naming.rmi,\
jdk.unsupported,jdk.crypto.ec \
    --strip-debug \
    --no-man-pages \
    --no-header-files \
    --compress=2 \
    --output /jre

# STAGE 2: Imagen final de Airflow
FROM apache/airflow:3.2.2

USER root

# Copiar el JRE recortado desde el stage anterior
COPY --from=jre-builder /jre /usr/lib/jvm/jre
ENV JAVA_HOME=/usr/lib/jvm/jre

# Instalar curl (necesario para healthchecks de los contenedores)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar Spark completo y en la MISMA capa eliminar lo no necesario.
# Al estar en la misma capa el espacio se libera realmente
# (a diferencia de la versión anterior donde rm -rf estaba en capa separada).
COPY spark-4.0.3-bin-hadoop3 /opt/spark
RUN rm -rf /opt/spark/R /opt/spark/data /opt/spark/examples /opt/spark/licenses /opt/spark/yarn \
    && rm -f /opt/spark/jars/hive-*.jar \
              /opt/spark/jars/spark-hive*.jar \
              /opt/spark/jars/spark-yarn*.jar \
              /opt/spark/jars/derby*.jar \
              /opt/spark/jars/datanucleus-*.jar \
              /opt/spark/jars/zookeeper-*.jar \
              /opt/spark/jars/curator-*.jar \
              /opt/spark/jars/avro-*.jar \
              /opt/spark/jars/orc-*.jar \
              /opt/spark/jars/spark-graphx*.jar \
              /opt/spark/jars/spark-mllib*.jar \
              /opt/spark/jars/spark-mllib-local*.jar \
    && rm -f /opt/spark/jars/netty-tcnative-*aarch_64*.jar \
              /opt/spark/jars/netty-tcnative-*osx*.jar \
              /opt/spark/jars/netty-tcnative-*windows*.jar

# Copiar driver JDBC de SQL Server dentro de los jars de Spark
COPY extra_jars/*.jar /opt/spark/jars/

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

USER airflow

# Instalar providers de Airflow necesarios para los DAGs
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark \
    apache-airflow-providers-microsoft-mssql \
    apache-airflow-providers-smtp \
    apache-airflow-providers-http \
    apache-airflow-providers-slack \
    apache-airflow-providers-openlineage \
    apache-airflow-providers-sftp

# ============================================================
# DOCKERFILE ANTERIOR (comentado)
# ============================================================
# FROM apache/airflow:3.2.2
# 
# USER root
# 
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     openjdk-17-jre-headless \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
# 
# COPY spark-4.0.3-bin-hadoop3 /opt/spark
# RUN rm -rf /opt/spark/R /opt/spark/data /opt/spark/examples /opt/spark/licenses
# COPY extra_jars/*.jar /opt/spark/jars/
# 
# ENV SPARK_HOME=/opt/spark
# ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# ENV PATH=$PATH:$SPARK_HOME/bin
# 
# USER airflow
# 
# RUN pip install --no-cache-dir \
#     apache-airflow-providers-apache-spark \
#     apache-airflow-providers-microsoft-mssql \
#     apache-airflow-providers-smtp \
#     apache-airflow-providers-http \
#     apache-airflow-providers-slack \
#     apache-airflow-providers-openlineage \
#     apache-airflow-providers-sftp
