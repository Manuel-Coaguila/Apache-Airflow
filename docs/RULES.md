# Reglas del equipo

## Scripts bash (`.sh`)

- Todo script debe comenzar con `#!/bin/bash` y `set -euo pipefail`
- Debe ser ejecutable: `chmod +x`
- Usar siempre variables con `"${VAR}"` (comillas dobles)
- Preferir `[[ ]]` en vez de `[ ]` para condiciones
- Logging con timestamp: `echo "[$(date)] [NOMBRE_SCRIPT] [LEVEL] mensaje"`
- Codigos de salida diferenciados (1, 2, 3... no solo 0/1)

## DAGs

- `dag.py` no debe superar ~60 lineas
- No hardcodear rutas usar variables de entorno con default
- Agregar siempre `tags` para filtrar en la UI de Airflow
- Toda tarea debe tener `retries` si es possible

## Commits

- Prefijo: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
- Mensajes en ingles o español consistente
- No commitear secretos ni archivos binarios

## Testing

- Cada proyecto debe tener `tests/test_dag.py`
- Ejecutar antes de mergear:
  ```bash
  docker compose run --rm airflow-cli python -m pytest dags/proyecto_NNN/tests/ -v
  ```
