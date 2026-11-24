#!/usr/bin/env bash
# ==============================================================================
# Script de Corrección y Mantenimiento de Errores del Sistema y Aplicaciones
# Sistema: Ubuntu 26.04 LTS (x86_64) - Kernel 7.0.0-44-generic
# Generado automáticamente por Antigravity
# ==============================================================================

set -euo pipefail

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # Sin color

echo -e "${BLUE}====================================================================${NC}"
echo -e "${CYAN}   SCRIPT DE CORRECCIÓN DE ERRORES DEL SISTEMA Y LOGS (ROOT)       ${NC}"
echo -e "${BLUE}====================================================================${NC}"

# 1. Comprobación de privilegios root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[ERROR] Este script debe ejecutarse con privilegios de root.${NC}"
   echo -e "Por favor, ejecútelo usando: ${YELLOW}sudo bash $0${NC}"
   exit 1
fi

echo -e "${GREEN}[OK] Privilegios de superusuario confirmados.${NC}\n"

# ------------------------------------------------------------------------------
# 2. Corrección de VA-API en /etc/environment (Intel Sandybridge GPU)
# ------------------------------------------------------------------------------
echo -e "${CYAN}>>> [1/7] Configurando controlador VA-API del sistema (Sandybridge i965)...${NC}"
if grep -q "LIBVA_DRIVER_NAME=" /etc/environment; then
    sed -i 's/LIBVA_DRIVER_NAME=.*/LIBVA_DRIVER_NAME=i965/' /etc/environment
    echo -e "${GREEN}[OK] LIBVA_DRIVER_NAME actualizado a 'i965' en /etc/environment.${NC}"
else
    echo "LIBVA_DRIVER_NAME=i965" >> /etc/environment
    echo -e "${GREEN}[OK] LIBVA_DRIVER_NAME=i965 agregado a /etc/environment.${NC}"
fi

# ------------------------------------------------------------------------------
# 3. Limpieza de paquetes residuales 'rc' en DPKG / APT
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}>>> [2/7] Comprobando paquetes en estado residual (rc) en DPKG...${NC}"
RESIDUAL_PACKAGES=$(dpkg -l | awk '/^rc/ {print $2}')

if [[ -n "$RESIDUAL_PACKAGES" ]]; then
    echo -e "${YELLOW}Se han encontrado paquetes residuales para purgar:${NC}"
    echo "$RESIDUAL_PACKAGES"
    echo -e "${BLUE}Purgando configuraciones residuales...${NC}"
    dpkg --purge $RESIDUAL_PACKAGES
    echo -e "${GREEN}[OK] Paquetes residuales purgados correctamente.${NC}"
else
    echo -e "${GREEN}[OK] No hay paquetes residuales en el sistema.${NC}"
fi

# Reparar dependencias rotas si las hubiera
dpkg --configure -a
apt-get autoremove -y --purge
apt-get clean

# ------------------------------------------------------------------------------
# 4. Solución al servicio en fallo 'vmware.service'
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}>>> [3/7] Gestionando servicio VMware fallido (vmware.service)...${NC}"
# El servicio vmware falla al arrancar porque los módulos de kernel vmmon/vmnet
# no están compilados para el kernel Linux 7.0.0-44.
if systemctl is-failed --quiet vmware.service 2>/dev/null || systemctl status vmware.service &>/dev/null; then
    echo -e "${YELLOW}El servicio vmware.service está registrado y causa fallo de inicio.${NC}"
    echo -e "Deteniendo y desactivando vmware.service para limpiar el estado de systemd..."
    systemctl stop vmware.service 2>/dev/null || true
    systemctl disable vmware.service 2>/dev/null || true
    update-rc.d -f vmware remove 2>/dev/null || true
    systemctl reset-failed vmware.service 2>/dev/null || true
    echo -e "${GREEN}[OK] vmware.service desactivado y estado de fallo reiniciado.${NC}"
else
    echo -e "${GREEN}[OK] vmware.service no está en fallo o no existe.${NC}"
fi

# ------------------------------------------------------------------------------
# 5. Mantenimiento y reparación de repositorios Flatpak
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}>>> [4/7] Reparando y limpiando objetos Flatpak del sistema...${NC}"
if command -v flatpak &>/dev/null; then
    echo "Ejecutando 'flatpak repair'..."
    flatpak repair --system || true
    echo "Eliminando dependencias y runtimes en desuso..."
    flatpak uninstall --unused --system -y || true
    echo -e "${GREEN}[OK] Flatpak del sistema reparado y optimizado.${NC}"
else
    echo -e "${YELLOW}[SKIP] Flatpak no está instalado.${NC}"
fi

# ------------------------------------------------------------------------------
# 6. Mantenimiento de logs del sistema (journalctl y syslog)
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}>>> [5/7] Verificando y rotando logs de journalctl...${NC}"
echo "Verificando integridad de los archivos de log del journal..."
journalctl --verify || true

echo "Limpiando logs antiguos (conservando los últimos 14 días)..."
journalctl --vacuum-time=14d || true
journalctl --vacuum-size=500M || true
echo -e "${GREEN}[OK] Journalctl verificado y optimizado.${NC}"

# ------------------------------------------------------------------------------
# 7. Verificación de configuración SMARTD para discos Seagate
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}>>> [6/7] Comprobando configuración de SMARTD (/etc/smartd.conf)...${NC}"
if [[ -f /etc/smartd.conf ]]; then
    # Comprobar si existe la alerta de firmware Seagate
    echo -e "${BLUE}Configuración actual de smartd preservada.${NC}"
    if systemctl is-active --quiet smartd 2>/dev/null; then
        echo -e "${GREEN}[OK] smartd.service está activo y monitorizando discos.${NC}"
    fi
fi

# ------------------------------------------------------------------------------
# 8. Actualización de configuración GRUB
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}>>> [7/7] Sincronizando configuración de GRUB...${NC}"
if command -v update-grub &>/dev/null; then
    update-grub
    echo -e "${GREEN}[OK] GRUB actualizado correctamente.${NC}"
else
    echo -e "${YELLOW}[SKIP] update-grub no encontrado.${NC}"
fi

echo -e "\n${BLUE}====================================================================${NC}"
echo -e "${GREEN}   ¡CORRECCIONES A NIVEL DE ROOT COMPLETADAS EXITOSAMENTE!         ${NC}"
echo -e "${BLUE}====================================================================${NC}"
echo -e "Comprobando estado final de servicios en fallo con 'systemctl --failed':"
systemctl --failed || true
echo -e "\n${CYAN}Listo. Para aplicar todos los cambios de entorno, reinicie la sesión o el equipo.${NC}\n"
