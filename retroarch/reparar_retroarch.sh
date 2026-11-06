#!/usr/bin/env bash
# ==============================================================================
# Script de Mantenimiento, Optimización y Reparación de RetroArch
# Plataforma: Flatpak org.libretro.RetroArch
# ==============================================================================

set -e

CONFIG_DIR="$HOME/.var/app/org.libretro.RetroArch/config/retroarch"
CONFIG_FILE="$CONFIG_DIR/retroarch.cfg"
LOG_DIR="$CONFIG_DIR/logs"

echo "========================================================"
echo "    Mantenimiento y Reparación de RetroArch            "
echo "========================================================"

# 1. Comprobar existencia de directorios
if [ ! -d "$CONFIG_DIR" ]; then
    echo "[ERROR] No se encontró el directorio de configuración de RetroArch en Flatpak:"
    echo "        $CONFIG_DIR"
    exit 1
fi

mkdir -p "$LOG_DIR"

# 2. Respaldo de la configuración actual
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="$CONFIG_DIR/retroarch.cfg.bak_$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "[1/4] Respaldo de retroarch.cfg creado:"
    echo "      -> $BACKUP_FILE"
fi

# 3. Corrección de URLs de descarga del Buildbot a HTTPS seguro
echo "[2/4] Actualizando URLs del Core Updater y Assets a HTTPS..."
if [ -f "$CONFIG_FILE" ]; then
    # Reemplazar http por https en URLs del buildbot de Libretro
    sed -i 's|http://buildbot.libretro.com|https://buildbot.libretro.com|g' "$CONFIG_FILE"
    echo "      -> URLs actualizadas a https://buildbot.libretro.com con éxito."
fi

# 4. Limpieza de logs antiguos y rotación
echo "[3/4] Saneando registros antiguos y temporales..."
if [ -f "$CONFIG_DIR/system/Mupen64plus/gliden64.log" ]; then
    > "$CONFIG_DIR/system/Mupen64plus/gliden64.log"
    echo "      -> Registro residual de GLideN64 limpiado."
fi

# 5. Sincronización y comprobación de permisos Flatpak
echo "[4/4] Comprobando permisos de dispositivos y sistema para RetroArch Flatpak..."
if command -v flatpak &>/dev/null; then
    # Asegurar acceso a udev y dispositivos para controladores/gamepads
    flatpak override --user --device=all org.libretro.RetroArch || true
    flatpak override --user --filesystem=/run/udev:ro org.libretro.RetroArch || true
    echo "      -> Permisos de gamepads y udev verificados para el usuario."
fi

echo "========================================================"
echo "    ¡Optimización y correcciones de RetroArch listas!   "
echo "========================================================"
