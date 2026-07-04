
# YA NO VA POR TEMAS DE SEGURIDAD


#!/bin/bash

# Spark
airflow connections delete spark_default || true
airflow connections add spark_default \
  --conn-type spark \
  --conn-host spark-master \
  --conn-port 7077 \
  --conn-extra '{"deploy-mode":"client","spark-binary":"spark-submit"}'

