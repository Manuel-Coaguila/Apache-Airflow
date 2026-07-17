# PIPELINES

Plataforma de orquestación de datos con **Apache Airflow 3.2.2** y **Apache Spark 4.0.3** en Docker.

## Stack

| Tecnología | Versión |
|---|---|
| Apache Airflow | 3.2.2 (CeleryExecutor) |
| Apache Spark | 4.0.3-bin-hadoop3 |
| Java | 17 (OpenJDK) |
| PostgreSQL | 16 |
| Redis | 7.2-bookworm |
| Docker Compose | — |

## Estructura

```
├── dags/                     Pipelines de Airflow
│   ├── common/               Código compartido entre proyectos
│   ├── check_connections/    DAG de utilidad (test de conexión)
│   ├── proyecto_001/         Proyecto ETL con Spark
│   └── proyecto_002/         Template para nuevo proyecto
├── docs/                     Documentación y convenciones
├── config/                   Configuración de Airflow
├── plugins/                  Plugins personalizados
├── Dockerfile                Imagen custom con Spark + JDBC
└── docker-compose.yaml       Servicios Airflow + PostgreSQL + Redis
```

## Requisitos

- Docker + Docker Compose
- Red externa `tesis-net` creada:
  ```bash
  docker network create tesis-net
  ```
- Archivo `.env` con las variables necesarias (ver `.env.example`)

## Inicio rápido

```bash
# Construir imagen
docker compose build

# Inicializar base de datos y crear usuario
docker compose up airflow-init

# Levantar todos los servicios
docker compose up -d
```

Airflow APIServer disponible en `http://localhost:8080`.

## Proyectos

Cada proyecto sigue la misma estructura:

```
proyecto_NNN/
├── dag.py                Orquestación (solo Airflow)
├── scripts/
│   ├── bash/             Scripts bash
│   └── sql/              Consultas SQL
└── tests/
    └── test_dag.py       Test del DAG
```

Los jobs Spark viven fuera de Airflow, en `/opt/spark/projects/proyecto_NNN/main.py`.

## Testing

```bash
docker compose run --rm airflow-cli python -m pytest dags/proyecto_001/tests/ -v
```

## Conexiones

| Conn ID | Tipo | Propósito |
|---|---|---|
| `spark_default` | Spark | Ejecutar jobs Spark |
| `mssql_default` | MSSQL | Conexión a SQL Server (opcional) |

## Documentación

- `docs/CONVENTIONS.md` — Naming y estructura de carpetas
- `docs/ARCHITECTURE.md` — Diagrama de flujo y componentes
- `docs/RULES.md` — Reglas del equipo
- `docs/adr/` — Architecture Decision Records

## Licencia

Apache 2.0
