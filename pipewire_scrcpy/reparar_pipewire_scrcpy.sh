#!/usr/bin/env bash
# ==============================================================================
# Script de corrección y optimización para PipeWire y scrcpy
# ==============================================================================
set -e

echo "=== Comprobando permisos de superusuario ==="
if [ "$EUID" -ne 0 ]; then
    echo "Este script necesita ejecutarse con sudo o como root."
    echo "Uso: sudo bash $0"
    exit 1
fi

echo ""
echo "[1/3] Instalando paquete libspa-0.2-libcamera para solucionar advertencia de WirePlumber..."
apt-get update -qq
apt-get install -y libspa-0.2-libcamera

echo ""
echo "[2/3] Verificando permisos udev para scrcpy y dispositivos Android..."
if ! dpkg -s android-udev-rules >/dev/null 2>&1; then
    echo "Instalando android-udev-rules..."
    apt-get install -y android-udev-rules
else
    echo "android-udev-rules ya está instalado."
fi

# Recargar reglas udev
udevadm control --reload-rules && udevadm trigger

echo ""
echo "[3/3] Reiniciando servicios de PipeWire para el usuario actual (si se invoca vía sudo)..."
if [ -n "$SUDO_USER" ]; then
    USER_ID=$(id -u "$SUDO_USER")
    echo "Reiniciando WirePlumber para el usuario $SUDO_USER (UID $USER_ID)..."
    sudo -u "$SUDO_USER" XDG_RUNTIME_DIR="/run/user/$USER_ID" systemctl --user restart wireplumber.service || true
fi

echo ""
echo "=== Correcciones aplicadas con éxito ==="
echo "Para verificar el estado de los servicios:"
echo "  systemctl --user status pipewire wireplumber pipewire-pulse"
echo "  wpctl status"
