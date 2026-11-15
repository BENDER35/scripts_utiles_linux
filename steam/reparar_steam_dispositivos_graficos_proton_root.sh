#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación de Steam (Permisos Root / Superusuario)
# Generado automáticamente para solucionar errores del sistema detectados en Steam
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}   Reparación y Optimización de Dependencias Steam   ${NC}"
echo -e "${BLUE}=====================================================${NC}"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[ERROR] Este script debe ejecutarse con privilegios de superusuario (root).${NC}"
    echo "Por favor ejecútalo como: sudo bash $0"
    exit 1
fi

echo -e "\n${YELLOW}[1/4] Instalando paquete steam-devices (Reglas udev para mandos)...${NC}"
if dpkg -s steam-devices >/dev/null 2>&1; then
    echo -e "${GREEN}[OK] steam-devices ya se encuentra instalado.${NC}"
else
    apt-get update -qq
    apt-get install -y steam-devices
    echo -e "${GREEN}[OK] steam-devices instalado correctamente.${NC}"
fi

echo -e "Recargando reglas de udev..."
udevadm control --reload-rules || true
udevadm trigger || true

echo -e "\n${YELLOW}[2/4] Instalando backend VDPAU-VAAPI para gráficos Intel (libvdpau-va-gl1)...${NC}"
# Corrige: Failed to open VDPAU backend libvdpau_va_gl.so
if dpkg -s libvdpau-va-gl1 >/dev/null 2>&1; then
    echo -e "${GREEN}[OK] libvdpau-va-gl1 ya está instalado.${NC}"
else
    apt-get install -y libvdpau-va-gl1
    echo -e "${GREEN}[OK] libvdpau-va-gl1 instalado correctamente.${NC}"
fi

echo -e "\n${YELLOW}[3/4] Configurando límites de descriptores de archivos (nofile) para Steam y Proton...${NC}"
LIMITS_FILE="/etc/security/limits.d/99-steam-limits.conf"
cat << 'EOF' > "$LIMITS_FILE"
# Configuración generada para Steam y Proton
# Aumenta el límite de descriptores de archivos para evitar fallos de esync / wine
*               soft    nofile          524288
*               hard    nofile          1048576
root            soft    nofile          524288
root            hard    nofile          1048576
EOF
echo -e "${GREEN}[OK] Archivo $LIMITS_FILE creado con límites optimizados.${NC}"

echo -e "\n${YELLOW}[4/4] Verificando variable de entorno LIBVA_DRIVER_NAME en /etc/environment...${NC}"
ENV_FILE="/etc/environment"
if [ -f "$ENV_FILE" ] && grep -q "^LIBVA_DRIVER_NAME=" "$ENV_FILE"; then
    echo "Se detectó LIBVA_DRIVER_NAME forzado a nivel global en $ENV_FILE."
    echo "Haciendo copia de seguridad en ${ENV_FILE}.bak..."
    cp "$ENV_FILE" "${ENV_FILE}.bak"
    # Comentar la línea para permitir la selección automática por parte de Mesa y FFmpeg
    sed -i 's/^LIBVA_DRIVER_NAME=/#LIBVA_DRIVER_NAME=/g' "$ENV_FILE"
    echo -e "${GREEN}[OK] Variable comentada en $ENV_FILE para evitar errores de inicialización en VA-API / OBS.${NC}"
else
    echo -e "${GREEN}[OK] /etc/environment no contiene variables conflictivas.${NC}"
fi

echo -e "\n${BLUE}=====================================================${NC}"
echo -e "${GREEN}  ¡Todas las reparaciones root han finalizado con éxito!  ${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo "Nota: Si modificaste límites del sistema, es recomendable cerrar sesión y volver a entrar."
