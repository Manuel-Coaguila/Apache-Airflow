# PIPELINES — Airflow + Spark

## Stack
- **Airflow** 3.2.2 (CeleryExecutor) con PostgreSQL + Redis
- **Spark** 4.0.3-bin-hadoop3 con Java 17
- **Docker** compose con imagen custom `airflow-custom:001`

## Servicios
| Servicio | Puerto | Comando |
|---|---|---|
| airflow-apiserver | 8080 | api-server |
| airflow-scheduler | — | scheduler |
| airflow-dag-processor | — | dag-processor |
| airflow-worker | — | celery worker |
| airflow-triggerer | — | triggerer |
| airflow-cli | — | (debug profile) |
| postgres | — | 16 |
| redis | 6379 | 7.2-bookworm |
| flower | 5555 | (flower profile) |

## DAGs existentes

| Archivo | DAG ID | Proposito |
|---|---|---|
| `dags/check_connections/dag.py` | `check_connections` | Test de conexion `spark_default` |
| `dags/proyecto_001/dag.py` | `proyecto_001_dag` | Mueve CSV del NAS a Spark y ejecuta `main.py` |
| `dags/proyecto_002/dag.py` | `proyecto_002_dag` | Placeholder para nuevo proyecto |

## Estructura de dags/

```
dags/
├── __init__.py
├── common/
│   ├── __init__.py
│   └── utils.py              Codigo compartido entre proyectos
├── check_connections/
│   ├── __init__.py
│   └── dag.py                DAG de utilidad (test de conexion)
├── proyecto_001/
│   ├── __init__.py
│   ├── dag.py                DAG principal del proyecto
│   ├── scripts/
│   │   ├── bash/
│   │   │   └── move_csv.sh   Script de copia CSV
│   │   └── sql/
│   └── tests/
│       ├── __init__.py
│       └── test_dag.py
└── proyecto_002/
    ├── __init__.py
    ├── dag.py                Template para nuevo proyecto
    ├── scripts/
    │   ├── bash/
    │   └── sql/
    └── tests/
        └── __init__.py
```

## Volumenes montados (host → contenedor)

| Host | Contenedor |
|---|---|
| `./dags` | `/opt/airflow/dags` |
| `./logs` | `/opt/airflow/logs` |
| `./config` | `/opt/airflow/config` |
| `./plugins` | `/opt/airflow/plugins` |
| `./ops` | `/opt/airflow/ops` |
| `~/Escritorio/Proyecto_Tesis/apache_spark/projects` | `/opt/spark/projects` |
| `~/Escritorio/Proyecto_Tesis/apache_spark/conf` | `/opt/spark/conf` |
| `~/Escritorio/Proyecto_Tesis/apache_spark/logs` | `/opt/spark/logs` |
| `~/Escritorio/Proyecto_Tesis/nas` | `/opt/airflow/nas` |

## Conexiones Airflow

| Conexión | Tipo | Host |
|---|---|---|
| `spark_default` | spark | spark-master:7077 |
| `mssql_default` | mssql | sql_server_2019:1433 |
| `postgres_default` | postgresql+psycopg2 | postgres:5432 |

Las conexiones se definen en `ops/connections/connections.json` y se crean via Python.

## Providers instalados (requirements.txt)
`apache-spark`, `standard`, `microsoft-mssql`, `smtp`, `http`, `slack`, `openlineage`, `sftp`, `pytest`

## Testing
```bash
docker compose run --rm airflow-cli python -m pytest dags/proyecto_001/tests/ -v
```

## Notas
- La red `tesis-net` debe existir externamente (`external: true`)
- El archivo `.env` debe contener `FERNET_KEY`, `AIRFLOW__API_AUTH__JWT_SECRET` y opcionalmente `_AIRFLOW_WWW_USER_USERNAME`/`_AIRFLOW_WWW_USER_PASSWORD`
- Cada proyecto sigue la misma estructura: `dag.py`, `scripts/{bash,sql}/`, `tests/`
- Los scripts `.sh` deben ser ejecutables (`chmod +x`)
- Para agregar un nuevo proyecto, copiar `proyecto_002/` y cambiar `dag_id`

## Estructura ops/

```
ops/
├── users/
│   ├── users.csv                    Lista de usuarios (CSV)
│   └── create_users.py              Creador batch de usuarios
├── connections/
│   ├── connections.json              Lista de conexiones (JSON)
│   └── create_connections.py        Creador batch de conexiones
└── env/                             Variables de entorno
```

## Usuarios y roles
- Roles por defecto: `Admin`, `User`, `Op`, `Viewer`
- `Op` permite ejecutar DAGs y ver logs; en Airflow 3.x tambien ve conexiones (solo lectura)

### Crear usuarios batch desde CSV
```bash
docker compose run --rm airflow-cli python /opt/airflow/ops/users/create_users.py
```

Las passwords se configuran en `ops/users/users.csv`. Cambiar `changeme` antes de ejecutar en produccion.

### Crear conexiones batch desde JSON
```bash
docker compose run --rm airflow-cli python /opt/airflow/ops/connections/create_connections.py
```
