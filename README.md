# PIPELINES

**Orquestación de datos simple, poderosa y lista para producción.**

Este proyecto nace con una idea clara: **que cualquier persona pueda aprender y usar tecnologías de datos modernas** (Apache Airflow + Apache Spark) sin importar si tiene un negocio, si maneja poca, media o mucha data, o si recién está empezando en el mundo de datos.

No necesitas ser un experto en infraestructura. Solo Docker y seguir los pasos.

---

## Filosofía

| Principio | Significado |
|---|---|
| **Simplicidad** | Que cualquier persona pueda clonar, configurar y ejecutar en su PC local sin dolores de cabeza |
| **Producción real** | Aunque es simple, usa las mismas herramientas y buenas prácticas que una empresa real: CeleryExecutor, PostgreSQL, Redis, Spark, Docker |
| **Escalable** | Cuando tu proyecto crezca, agregar más workers o réplicas es cambiar un número |
| **Aprendizaje** | El objetivo final es que entiendas cómo funciona un ecosistema de datos real y puedas sobresalir profesionalmente |

---

## Stack

| Tecnología | Versión | ¿Para qué? |
|---|---|---|
| Apache Airflow | 3.2.2 (CeleryExecutor) | Orquestar los pipelines (DAGs) |
| Apache Spark | 4.0.3-bin-hadoop3 | Procesar datos pesados (ETL, transformaciones) |
| Java | 17 (OpenJDK) | Requerido por Spark |
| PostgreSQL | 16 | Base de datos interna de Airflow |
| Redis | 7.2-bookworm | Broker de mensajería para Celery |
| Celery | — | Ejecutar tareas en paralelo (workers) |
| Docker Compose | — | Levantar todo con un solo comando |

---

## Estructura del proyecto

```
├── dags/                          Tus pipelines (DAGs de Airflow)
│   ├── common/                    Código compartido entre proyectos
│   ├── check_connections/         DAG para probar conexiones
│   ├── proyecto_001/              Proyecto ETL completo (CSV → Spark → SQL Server)
│   └── proyecto_002/              Template listo para copiar
├── config/
│   └── airflow.cfg                Configuración de Airflow
├── ops/
│   ├── connections/               Conexiones a bases de datos
│   └── users/                     Usuarios del sistema
├── docs/                          Reglas, convenciones y arquitectura
├── Dockerfile                     Imagen con Airflow + Spark + JDBC
└── docker-compose.yaml            Todos los servicios definidos aquí
```

---

## Inicio rápido (5 minutos)

### Requisitos

- Docker + Docker Compose v2
- Git
- 4 GB de RAM libre (mínimo)

### Paso a paso

```bash
# 1. Clonar
git clone <tu-repo> pipelines
cd pipelines

# 2. Crear la red externa (solo la primera vez)
docker network create tesis-net

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores (o dejar los default para desarrollo local)

# 4. Construir la imagen
docker compose build

# 5. Inicializar base de datos y crear usuario admin
docker compose up airflow-init

# 6. ¡Levantar todo!
docker compose up -d
```

Airflow APIServer disponible en **http://localhost:8080**.

### Usuario admin por defecto

| Campo | Valor |
|---|---|
| Usuario | `airflow` |
| Password | `airflow` |

(Puedes cambiarlos en `.env`)

---

## ¿Qué hace cada servicio?

| Servicio | Contenedor | Función |
|---|---|---|
| `airflow-apiserver` | `airflow_airflow-apiserver_1` | UI web y API REST |
| `airflow-scheduler` | `airflow_airflow-scheduler_1` | Dispara los DAGs según su schedule |
| `airflow-worker` | `airflow_airflow-worker_1` | Ejecuta las tareas de los DAGs |
| `airflow-dag-processor` | `airflow_airflow-dag-processor_1` | Escanea y parsea los archivos de DAG |
| `airflow-triggerer` | `airflow_airflow-triggerer_1` | Maneja tareas diferidas (sensores) |
| `postgres` | `airflow_postgres_1` | Base de datos metadata de Airflow |
| `redis` | `airflow_redis_1` | Broker de mensajería Celery |
| `airflow-init` | `airflow_airflow-init_1` | Se ejecuta una vez al inicio (inicializa BD y crea admin) |
| `airflow-cli` | `airflow_airflow-cli_1` | Línea de comandos (solo debug) |
| `flower` | `airflow_flower_1` | Monitoreo visual de Celery (perfil opcional) |

---

## Mejoras aplicadas (producción simulada)

| Mejora | ¿Qué cambiamos? | Beneficio |
|---|---|---|
| **Claves en .env** | `secret_key` y `jwt_secret` ahora viajan en `.env` | No hay secrets hardcodeados en el cfg |
| **Workers API** | Subido de 1 a 4 | La UI responde mejor con múltiples usuarios |
| **Parsing de DAGs** | Subido de 2 a 4 procesos en paralelo | Los DAGs se actualizan más rápido |
| **Container naming** | Prefijo `airflow_` en todos los contenedores | Nombres predecibles y escalables |
| **Escalabilidad lista** | Compatible con `replicas` sin tocar config | Agregar workers es cambiar un número |
| **HA-ready** | `use_row_level_locking = True` | Múltiples schedulers pueden coexistir |

---

## Crear un nuevo proyecto

Cada proyecto es autónomo. Solo copia `proyecto_002/` y cambia el `dag_id`:

```
dags/mi_proyecto/
├── __init__.py
├── dag.py                ← Aquí defines las tareas
├── scripts/
│   ├── bash/             ← Scripts shell
│   └── sql/              ← Consultas SQL
└── tests/
    ├── __init__.py
    └── test_dag.py       ← Pruebas del DAG
```

**Regla de oro**: el `dag.py` solo orquesta (tareas, dependencias, tiempos). La lógica pesada va en scripts bash o jobs Spark.

---

## Testing

```bash
docker compose run --rm airflow-cli python -m pytest dags/proyecto_001/tests/ -v
```

---

## Conexiones disponibles

| Conn ID | Tipo | Host | ¿Para qué? |
|---|---|---|---|
| `spark_default` | Spark | spark-master:7077 | Ejecutar jobs Spark |
| `mssql_default` | MSSQL | sql_server_2019:1433 | Leer/escribir en SQL Server |
| `postgres_default` | PostgreSQL | postgres:5432 | Consultar metadata de Airflow |

Para crear las conexiones:
```bash
docker compose run --rm airflow-cli python /opt/airflow/ops/connections/create_connections.py
```

---

## Usuarios y roles

Puedes crear usuarios batch desde un CSV:

```bash
docker compose run --rm airflow-cli python /opt/airflow/ops/users/create_users.py
```

| Rol | Permisos |
|---|---|
| `Admin` | Todo |
| `Op` | Ejecutar DAGs, ver logs, ver conexiones |
| `User` | Ver y ejecutar DAGs |
| `Viewer` | Solo lectura |

Los usuarios se definen en `ops/users/users.csv`. Cambia las passwords antes de producción.

---

## Escalar (cuando tu proyecto crezca)

```yaml
# En docker-compose.yaml, solo cambia replicas:
airflow-worker:
  deploy:
    replicas: 4   # Ahora tienes 4 workers ejecutando tareas en paralelo
```

Docker se encarga del resto. Los nombres serán `airflow_airflow-worker_1`, `_2`, `_3`, `_4`.

---

## Documentación relacionada

- `docs/CONVENTIONS.md` — Convenciones de nomenclatura
- `docs/ARCHITECTURE.md` — Diagrama de flujo
- `docs/RULES.md` — Reglas de código y commits
- `docs/adr/` — Decisiones de arquitectura

---

## ¿Por qué este proyecto?

Porque las herramientas de datos no deberían ser solo para grandes empresas con equipos de infraestructura.

**Si puedes clonar un repo y ejecutar `docker compose up`, puedes tener tu propio ecosistema de datos profesional funcionando en tu PC.** Aprende, experimenta, equivócate, y cuando llegues a una empresa real, ya sabrás cómo funciona.

---

## Licencia

Apache 2.0
