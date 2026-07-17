# Convenciones del proyecto

## Nombres

| Elemento | Convencion | Ejemplo |
|---|---|---|
| Proyectos | `snake_case` con prefijo `proyecto_` | `proyecto_001`, `proyecto_002` |
| Archivos DAG | siempre `dag.py` | `proyecto_001/dag.py` |
| `dag_id` | `snake_case` con sufijo `_dag` | `proyecto_001_dag`, `check_connections` |
| `task_id` | `snake_case` | `move_file_csv`, `read_sqlserver_table` |
| Scripts bash | `snake_case` con extension `.sh` | `move_csv.sh` |
| Scripts sql | `snake_case` con extension `.sql` | `extract_clientes.sql` |
| Variables de entorno | `UPPER_SNAKE_CASE` | `CSV_ORIGEN`, `CSV_DESTINO` |
| Funciones Python | `snake_case` | `test_connection`, `log_error` |

## Estructura de cada proyecto

```
proyecto_NNN/
├── __init__.py
├── dag.py                  solo orquestacion, < 60 lineas
├── scripts/
│   ├── bash/               scripts bash
│   └── sql/                consultas SQL
└── tests/
    ├── __init__.py
    └── test_dag.py          test de importacion del DAG
```

## Reglas generales

- `dag.py` solo orquesta NUNCA contiene logica de negocio
- La logica pesada va fuera: Spark (`main.py` en `/opt/spark/projects/`), scripts bash, etc.
- Los scripts `.sh` deben tener `set -euo pipefail` y `chmod +x`
- Usar ingles para nombres de variables en codigo español solo para logs de usuario final
- `__init__.py` obligatorio en cada subcarpeta Python
