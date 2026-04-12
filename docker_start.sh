#!/bin/bash

# Script para automatizar el inicio de Docker y la gestión de .env

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}    Iniciando Despliegue Docker        ${NC}"
echo -e "${BLUE}=======================================${NC}"

# 1. Comprobar si existe .env
if [ ! -f .env ]; then
    echo -e "Archivo .env no encontrado. Generando desde plantilla..."
    if [ -f .env.example ]; then
        cp .env.example .env
        
        # Generar una SECRET_KEY aleatoria usando Python 3
        if command -v python3 &> /dev/null; then
            NEW_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
            # Reemplazar la línea de SECRET_KEY en el .env
            # Usamos sed para buscar la línea que empieza por SECRET_KEY= y reemplazarla
            # macOS requiere '' después de -i para trabajar correctamente
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/^SECRET_KEY=.*/SECRET_KEY=$NEW_KEY/" .env
            else
                sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$NEW_KEY/" .env
            fi
            echo -e "${GREEN}✓ Archivo .env creado con una SECRET_KEY nueva.${NC}"
        else
            echo -e "${RED}Aviso: No se pudo generar una SECRET_KEY aleatoria (python3 no disponible). Se usará el valor por defecto.${NC}"
        fi
    else
        echo -e "${RED}Error: No se encuentra .env.example para generar el entorno.${NC}"
        exit 1
    fi
else
    echo -e "Archivo .env detectado. Usando configuración existente."
fi

# 2. Lanzar docker-compose
echo -e "${BLUE}Levantando servicios con Docker Compose...${NC}"
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}=======================================${NC}"
    echo -e "${GREEN}   ¡Despliegue completado con éxito!   ${NC}"
    echo -e "${GREEN}   Accede en: http://localhost         ${NC}"
    echo -e "${GREEN}=======================================${NC}"
else
    echo -e "${RED}Hubo un error al levantar los contenedores.${NC}"
    exit 1
fi
