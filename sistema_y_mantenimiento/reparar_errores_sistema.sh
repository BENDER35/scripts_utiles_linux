#!/usr/bin/env bash
# ==============================================================================
# Script de Corrección de Errores, Advertencias y Mantenimiento del Sistema
# Ejecutar como root o con sudo: sudo ./reparar_errores_sistema.sh
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[ERROR] Este script debe ejecutarse con privilegios de superusuario (sudo/root).${NC}"
   echo "Uso: sudo $0"
   exit 1
fi

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}   INICIANDO CORRECCIÓN DE ERRORES Y ADVERTENCIAS DEL SISTEMA   ${NC}"
echo -e "${BLUE}================================================================${NC}"

# 1. Limpieza de reportes de error obsoletos en /var/crash
echo -e "\n${YELLOW}[1/9] Limpiando reportes de fallos obsoletos en /var/crash...${NC}"
if [ -d /var/crash ]; then
    CRASH_COUNT=$(find /var/crash -type f | wc -l)
    if [ "$CRASH_COUNT" -gt 0 ]; then
        rm -rf /var/crash/*
        echo -e "${GREEN}[OK] Se eliminaron $CRASH_COUNT archivos antiguos de /var/crash.${NC}"
    else
        echo -e "${GREEN}[OK] El directorio /var/crash ya está limpio.${NC}"
    fi
fi

# 2. Corrección de advertencia udev: convertir 'uinput' a grupo de sistema (<1000)
echo -e "\n${YELLOW}[2/9] Corrigiendo GID del grupo 'uinput' a grupo de sistema...${NC}"
if getent group uinput >/dev/null; then
    CURRENT_GID=$(getent group uinput | cut -d: -f3)
    if [ "$CURRENT_GID" -ge 1000 ]; then
        groupmod -g 980 uinput || true
        echo -e "${GREEN}[OK] Grupo 'uinput' modificado a GID de sistema (980).${NC}"
    else
        echo -e "${GREEN}[OK] El grupo 'uinput' ya es un grupo de sistema (GID $CURRENT_GID).${NC}"
    fi
fi

# 3. Corrección de advertencias D-Bus: usuarios de servicio para malcontent
echo -e "\n${YELLOW}[3/9] Creando usuarios de sistema para servicios de malcontent (D-Bus)...${NC}"
for user in malcontent-timerd malcontent-webd malcontent-timer-ext-agent; do
    if ! id -u "$user" >/dev/null 2>&1; then
        useradd -r -s /usr/sbin/nologin -d /nonexistent -M "$user" || true
        echo -e "${GREEN}[OK] Usuario de sistema '$user' creado para D-Bus.${NC}"
    else
        echo -e "${GREEN}[OK] El usuario '$user' ya existe.${NC}"
    fi
done

# 4. Restablecimiento y recarga de systemd y servicios
echo -e "\n${YELLOW}[4/9] Recargando demonios de systemd y restableciendo unidades...${NC}"
systemctl daemon-reload
systemctl reset-failed || true
if systemctl is-enabled apport.service &>/dev/null; then
    systemctl restart apport.service || true
fi
systemctl restart apport-autoreport.service || true
if systemctl is-active --quiet rsyslog.service; then
    systemctl restart rsyslog.service || true
fi
echo -e "${GREEN}[OK] Systemd recargado. Estado de unidades fallidas:${NC}"
systemctl --failed --no-pager

# 5. Reparación y optimización de paquetes APT / DPKG
echo -e "\n${YELLOW}[5/9] Verificando y saneando paquetería APT/DPKG...${NC}"
dpkg --configure -a
apt-get install -f -y
apt-get autoremove --purge -y
apt-get autoclean -y
apt-get clean
echo -e "${GREEN}[OK] Paquetería APT saneada correctamente.${NC}"

# 6. Mantenimiento y verificación de Flatpak
echo -e "\n${YELLOW}[6/9] Verificando e indexando Flatpak del sistema...${NC}"
if command -v flatpak &>/dev/null; then
    flatpak repair || true
    flatpak uninstall --unused -y || true
    echo -e "${GREEN}[OK] Flatpak verificado y saneado.${NC}"
else
    echo -e "${BLUE}[INFO] Flatpak no está instalado.${NC}"
fi

# 7. Mantenimiento y refresco de Snap
echo -e "\n${YELLOW}[7/9] Verificando estado y refrescando paquetes Snap...${NC}"
if command -v snap &>/dev/null; then
    snap refresh || true
    echo -e "${GREEN}[OK] Snaps comprobados y actualizados.${NC}"
else
    echo -e "${BLUE}[INFO] Snap no está instalado.${NC}"
fi

# 8. Verificación de permisos de usuario (vboxusers y uinput)
echo -e "\n${YELLOW}[8/9] Verificando grupos de usuario (vboxusers, uinput)...${NC}"
TARGET_USER="${SUDO_USER:-bender}"
if id "$TARGET_USER" &>/dev/null; then
    if getent group vboxusers &>/dev/null; then
        usermod -aG vboxusers "$TARGET_USER"
    fi
    if getent group uinput &>/dev/null; then
        usermod -aG uinput "$TARGET_USER"
    fi
    echo -e "${GREEN}[OK] Usuario $TARGET_USER verificado en vboxusers y uinput.${NC}"
fi

# 9. Recarga de reglas udev, optimización de journald y actualización de GRUB
echo -e "\n${YELLOW}[9/9] Recargando udev, optimizando journald y actualizando GRUB...${NC}"
udevadm control --reload-rules || true
udevadm trigger || true
journalctl --vacuum-time=14d || true
if command -v update-grub &>/dev/null; then
    update-grub || true
    echo -e "${GREEN}[OK] Configuración de GRUB actualizada.${NC}"
fi

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${GREEN}¡Correcciones de errores y advertencias completadas con éxito!${NC}"
echo -e "${BLUE}================================================================${NC}"
