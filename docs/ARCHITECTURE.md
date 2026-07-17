# Arquitectura

## Diagrama de flujo

```
NAS (host)
  │
  │  volumen: ~/nas -> /opt/airflow/nas
  │
  ▼
Airflow DAG (proyecto_001/dag.py)
  │
  ├── BashOperator: move_csv.sh
  │     copia CSV del NAS a /opt/spark/projects/.../input/
  │
  ├── SparkSubmitOperator: main.py
  │     ejecuta Spark job contra SQL Server
  │
  └── BashOperator: fin
```

## Componentes

### Airflow
- Orquesta los pipelines via DAGs
- Los DAGs estan en `dags/` montados como volumen
- Usa CeleryExecutor con PostgreSQL + Redis

### Spark
- Los jobs Spark viven en `/opt/spark/projects/proyecto_NNN/main.py`
- El directorio `projects/` se monta desde `~/apache_spark/projects`
- Driver JDBC de SQL Server en `/opt/spark/jars/`

### Volumenes clave

| Host | Contenedor | Proposito |
|---|---|---|
| `./dags` | `/opt/airflow/dags` | Codigo de los DAGs |
| `~/nas` | `/opt/airflow/nas` | Archivos CSV de entrada |
| `~/apache_spark/projects` | `/opt/spark/projects` | Jobs de Spark |
| `~/apache_spark/conf` | `/opt/spark/conf` | Configuracion Spark |
| `~/apache_spark/logs` | `/opt/spark/logs` | Logs de Spark |

## Red
- Todos los servicios en `tesis-net` (externa, `external: true`)
- Airflow APIServer expuesto en puerto `8080`
