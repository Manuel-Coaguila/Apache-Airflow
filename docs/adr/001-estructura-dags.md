# ADR-001: Estructura de carpetas dentro de dags/

## Contexto
El proyecto necesita soportar multiples proyectos independientes (ETLs, conexiones, etc.) dentro de Airflow.

## Decision
Se adopta la siguiente estructura:

```
dags/
├── common/               codigo compartido
├── check_connections/    DAGs transversales
├── proyecto_NNN/         un proyecto = una carpeta
│   ├── dag.py            orquestacion pura
│   ├── scripts/
│   │   ├── bash/
│   │   └── sql/
│   └── tests/
```

## Consecuencias
- Cada proyecto es autocontenido y copiable
- DAGs transversales separados de proyectos de negocio
- imports simples: `from common.utils import X`
