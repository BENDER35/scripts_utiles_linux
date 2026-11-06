#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación y Mantenimiento de DPKG y APT
# ==============================================================================
# Este script realiza un mantenimiento integral del gestor de paquetes (dpkg/apt),
# solucionando configuraciones incompletas, dependencias rotas, purgando paquetes
# residuales en estado 'rc', recargando servicios del sistema y optimizando la caché.
# ==============================================================================

set -euo pipefail

# Colores para salida por terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

echo -e "${BLUE}=== Iniciando Diagnóstico y Reparación de DPKG / APT ===${NC}\n"

# 1. Verificar si se ejecuta como root / superusuario
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Error: Este script debe ejecutarse con privilegios de superusuario (sudo).${NC}"
  echo -e "Uso: sudo $0"
  exit 1
fi

# 2. Configurar paquetes pendientes o a medio configurar
echo -e "${BLUE}[1/6] Comprobando paquetes pendientes de configuración...${NC}"
if dpkg --configure -a; then
  echo -e "${GREEN}[✓] dpkg --configure -a completado sin errores.${NC}\n"
else
  echo -e "${RED}[!] Hubo un error al configurar paquetes pendientes.${NC}\n"
fi

# 3. Reparar dependencias rotas si las hubiese
echo -e "${BLUE}[2/6] Verificando y reparando dependencias rotas (apt-get --fix-broken install)...${NC}"
if apt-get --fix-broken install -y; then
  echo -e "${GREEN}[✓] Dependencias verificadas y reparadas correctamente.${NC}\n"
else
  echo -e "${RED}[!] Error al intentar reparar dependencias.${NC}\n"
fi

# 4. Purgar paquetes residuales en estado 'rc' (archivos de configuración huérfanos)
echo -e "${BLUE}[3/6] Buscando paquetes en estado 'rc' (removidos pero con configuración)...${NC}"
RC_PACKAGES=$(dpkg -l | awk '/^rc/ {print $2}')

if [ -n "$RC_PACKAGES" ]; then
  echo -e "${YELLOW}[!] Se encontraron paquetes residuales:${NC}"
  echo "$RC_PACKAGES"
  echo -e "${BLUE}Purgando configuraciones residuales...${NC}"
  # Purgar los paquetes
  # shellcheck disable=SC2086
  dpkg --purge $RC_PACKAGES
  echo -e "${GREEN}[✓] Paquetes residuales purgados correctamente.${NC}\n"
else
  echo -e "${GREEN}[✓] No se encontraron paquetes en estado residual ('rc').${NC}\n"
fi

# 5. Limpiar directorios de módulos huérfanos de kernels antiguos desinstalados
echo -e "${BLUE}[4/6] Verificando directorios huérfanos en /usr/lib/modules/...${NC}"
CURRENT_KERNEL=$(uname -r)
INSTALLED_KERNELS=$(dpkg -l | grep -E '^ii\s+linux-(image|modules)-' | awk '{print $2}' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic' | sort -u || true)

for mod_dir in /usr/lib/modules/*; do
  if [ -d "$mod_dir" ]; then
    kver=$(basename "$mod_dir")
    # Si la versión no es la del kernel actual y no está en la lista de instalados
    if [ "$kver" != "$CURRENT_KERNEL" ] && ! echo "$INSTALLED_KERNELS" | grep -qw "$kver"; then
      echo -e "${YELLOW}[!] Directorio de módulos huérfano detectado: $mod_dir${NC}"
      # Solo borrar si no contiene módulos activos ni paquetes registrados
      rm -rf "$mod_dir"
      echo -e "${GREEN}[✓] Eliminado directorio huérfano: $mod_dir${NC}"
    fi
  fi
done
echo -e "${GREEN}[✓] Verificación de módulos completada.${NC}\n"

# 6. Recargar systemd y limpiar estados fallidos (advertencia de rsyslog y triggers)
echo -e "${BLUE}[5/6] Recargando configuración de systemd y reseteando unidades fallidas...${NC}"
systemctl daemon-reload
systemctl reset-failed || true
echo -e "${GREEN}[✓] systemctl daemon-reload ejecutado con éxito.${NC}\n"

# 7. Autoremove y limpieza de caché de paquetes obsoletos
echo -e "${BLUE}[6/6] Limpiando paquetes obsoletos y caché de APT...${NC}"
apt-get autoremove -y --purge
apt-get clean
echo -e "${GREEN}[✓] Limpieza del sistema finalizada.${NC}\n"

echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}¡Proceso de reparación y mantenimiento completado con éxito!${NC}"
echo -e "${GREEN}======================================================${NC}"
