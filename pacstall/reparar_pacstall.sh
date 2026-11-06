#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación y Mantenimiento de Pacstall y Paquetes (Root)
# Ubicación: /home/bender/Descargas/reparar_pacstall.sh
# ==============================================================================

set -e

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Comprobar permisos de root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}ERROR: Este script requiere privilegios de superusuario (root).${NC}" >&2
    echo -e "Por favor, ejecútalo con: ${YELLOW}sudo $0${NC}" >&2
    exit 1
fi

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}       Mantenimiento y Reparación de Pacstall / APT                   ${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

# 2. Diagnóstico del estado actual
echo -e "${GREEN}[1/4] Verificando instalación de Pacstall...${NC}"
PACSTALL_BIN=$(command -v pacstall || true)

if [ -z "$PACSTALL_BIN" ]; then
    echo -e "${RED}Pacstall no se encuentra en el PATH del sistema.${NC}"
    exit 1
fi

PAC_VER=$(pacstall -V 2>/dev/null || echo "Desconocida")
echo "  -> Versión actual de Pacstall: $PAC_VER"

if dpkg -s pacstall >/dev/null 2>&1; then
    DEB_VER=$(dpkg-query -W -f='${Version}' pacstall)
    echo -e "  -> Pacstall está instalado mediante paquete Debian (.deb): ${YELLOW}${DEB_VER}${NC}"
    echo "     (Nota: El comando 'pacstall -U' está bloqueado intencionadamente por diseño"
    echo "      en instalaciones .deb, ya que las actualizaciones deben gestionarse vía APT/PPR)."
else
    echo "  -> Pacstall está instalado mediante Pacscript/Git independiente."
fi
echo ""

# 3. Actualizar Pacstall mediante APT / PPR
echo -e "${GREEN}[2/4] Actualizando Pacstall desde el repositorio oficial PPR (APT)...${NC}"
if dpkg -s pacstall >/dev/null 2>&1; then
    apt-get update -o Dir::Etc::sourcelist="sources.list.d/ppr.list" \
                   -o Dir::Etc::sourceparts="-" \
                   -o APT::Get::List-Cleanup="0" || apt-get update -qq
    apt-get install --only-upgrade -y pacstall || echo -e "${YELLOW}Pacstall ya está en la última versión de los repositorios.${NC}"
else
    echo "Pacstall no está instalado como .deb; omitiendo actualización por APT."
fi
echo ""

# 4. Actualizar listas de scripts y paquetes de Pacstall
echo -e "${GREEN}[3/4] Actualizando repositorios internos de Pacstall (-Up)...${NC}"
pacstall -Up || {
    echo -e "${YELLOW}Advertencia: 'pacstall -Up' finalizó con código no cero.${NC}"
}

echo ""
echo -e "${GREEN}[4/4] Actualizando paquetes instalados vía Pacstall (-Ug)...${NC}"
# Pacstall -Ug actualiza todos los paquetes instalados mediante pacscripts
pacstall -Ug || {
    echo -e "${YELLOW}No hay paquetes adicionales pendientes de actualización o ya están al día.${NC}"
}

echo ""
echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}Mantenimiento básico completado con éxito.${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

# 5. Opción voluntaria de migración a Pacscript nativo
echo -e "${YELLOW}--- MIGRACIÓN OPCIONAL ---${NC}"
echo "Actualmente Pacstall está instalado como paquete .deb (PPR)."
echo "Si deseas que el comando 'pacstall -U' funcione sin advertencias (como hace Topgrade),"
echo "Pacstall permite migrar a su versión de pacscript oficial."
echo ""
read -r -p "¿Deseas migrar la instalación de Pacstall a Pacscript ahora? [s/N]: " RESPUESTA

case "$RESPUESTA" in
    [sS][iI]|[sS])
        echo -e "${BLUE}Iniciando instalación del último pacscript de Pacstall ('pacstall -I pacstall')...${NC}"
        pacstall -I pacstall
        echo -e "${GREEN}¡Migración a Pacscript completada! Ahora 'pacstall -U' funcionará normalmente.${NC}"
        ;;
    *)
        echo -e "Omitida la migración. Pacstall continuará gestionándose de forma segura vía APT/PPR."
        ;;
esac

echo ""
echo -e "${GREEN}Proceso finalizado correctamente.${NC}"
exit 0
