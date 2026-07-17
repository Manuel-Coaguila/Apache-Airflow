#!/bin/bash
# ==============================================================================
# move_csv.sh
# -----------
# Copia un archivo CSV desde el NAS hacia el directorio de entrada de Spark,
# con validaciones pre y post transferencia para garantizar integridad.
#
# USO:
#   ./move_csv.sh
#   CSV_ORIGEN=/ruta/origen.csv CSV_DESTINO=/ruta/destino.csv ./move_csv.sh
#
# VARIABLES DE ENTORNO (opcionales):
#   CSV_ORIGEN   Ruta del archivo origen  (default: /opt/airflow/nas/Proyecto_001/Employee.csv)
#   CSV_DESTINO  Ruta del archivo destino (default: /opt/spark/projects/.../Employee.csv)
#
# CODIGOS DE SALIDA:
#   0    Transferencia exitosa
#   1    Archivo origen no encontrado
#   2    Archivo origen vacio
#   3    Espacio insuficiente en disco destino
#   4    Error de copia o integridad
#
# DEPENDENCIAS:
#   - coreutils (stat, df, mkdir, cp)
#
# LOGS:
#   Salida formateada con timestamp y nombre de script para trazabilidad en Airflow.
# ==============================================================================

set -euo pipefail

# ==============================================================================
# CONSTANTES
# ==============================================================================
SCRIPT="move_csv"

# ==============================================================================
# VALIDACION DE DEPENDENCIAS
# ==============================================================================
for cmd in stat df mkdir cp dirname; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$SCRIPT] ERROR: Comando no encontrado: $cmd"
        exit 99
    fi
done

# ==============================================================================
# CONFIGURACION
# ==============================================================================
ORIGEN="${CSV_ORIGEN:-/opt/airflow/nas/Proyecto_001/Employee.csv}"
DESTINO="${CSV_DESTINO:-/opt/spark/projects/proyecto_001/files/input/Employee.csv}"

log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$SCRIPT] [$level] $*"
}

# ==============================================================================
# VALIDACIONES PREVIAS
# ==============================================================================
log "INFO" "Iniciando copia: $ORIGEN -> $DESTINO"

# Validar que el archivo origen existe
if [ ! -f "$ORIGEN" ]; then
    log "ERROR" "Archivo origen no encontrado: $ORIGEN"
    exit 1
fi

# Validar que el archivo origen no este vacio
if [ ! -s "$ORIGEN" ]; then
    log "ERROR" "Archivo origen vacio: $ORIGEN"
    exit 2
fi

# Crear directorio destino recursivamente
mkdir -p "$(dirname "$DESTINO")"

FILE_SIZE=$(stat --format=%s "$ORIGEN")

# Validar espacio disponible en disco destino
DEST_DISK=$(df --output=avail "$(dirname "$DESTINO")" | tail -1)
if [ "$FILE_SIZE" -ge "$DEST_DISK" ]; then
    log "ERROR" "Espacio insuficiente en $(dirname "$DESTINO"): disponible=$DEST_DISK requerido=$FILE_SIZE"
    exit 3
fi

# ==============================================================================
# TRANSFERENCIA
# ==============================================================================
log "INFO" "Copiando archivo ($FILE_SIZE bytes)..."
cp "$ORIGEN" "$DESTINO"

# ==============================================================================
# VALIDACION POST-TRANSFERENCIA
# ==============================================================================
DEST_SIZE=$(stat --format=%s "$DESTINO")
if [ "$FILE_SIZE" -ne "$DEST_SIZE" ]; then
    log "ERROR" "Falló integridad: origen=$FILE_SIZE destino=$DEST_SIZE"
    exit 4
fi

log "INFO" "Archivo copiado exitosamente ($FILE_SIZE bytes)"
