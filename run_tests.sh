#!/bin/bash

# Script para ejecutar los tests de ProyectoDAW de forma independiente

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   Ejecución de Tests - ProyectoDAW    ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Obtener el directorio donde residen los tests (asumiendo que este script está en la raíz)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$PROJECT_DIR"

# Verificar entorno virtual
if [ -d ".venv" ]; then
    echo -e "Encontrado entorno virtual .venv, activando..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo -e "Encontrado entorno virtual venv, activando..."
    source venv/bin/activate
else
    echo -e "${RED}Error: No se encontró la carpeta .venv o venv.${NC}"
    echo "Asegúrate de haber creado el entorno virtual con: python -m venv .venv"
    exit 1
fi

# Instalar pytest si no está (opcional, pero útil para independencia total)
if ! command -v pytest &> /dev/null; then
    echo "pytest no encontrado en el entorno virtual, intentando instalar..."
    pip install pytest pytest-flask mongomock flask python-dotenv
fi

echo -e "${GREEN}Iniciando ejecución de pruebas con pytest...${NC}"
echo "---------------------------------------"

# Ejecutar pytest
# Usamos el path completo a pytest dentro del venv por seguridad
./.venv/bin/pytest -v --disable-warnings

# Capturar resultado
RESULT=$?

echo "---------------------------------------"
if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}¡ÉXITO! Todos los tests han pasado.${NC}"
else
    echo -e "${RED}FALLO en las pruebas. Revisa los errores arriba.${NC}"
fi

echo -e "${BLUE}=======================================${NC}"

# Salir con el mismo código que pytest
exit $RESULT
