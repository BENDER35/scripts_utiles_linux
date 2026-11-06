#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación: Wayland, Waydroid y OBS Studio
# Sistema detectado: Ubuntu 26.04 LTS (x86_64) - Intel HD Graphics 2000 (Sandy Bridge)
# ==============================================================================

set -euo pipefail

# Comprobar privilegios de root
if [ "$(id -u)" -ne 0 ]; then
    echo "[-] ERROR: Este script debe ejecutarse con privilegios de root (sudo)."
    echo "    Uso: sudo $0"
    exit 1
fi

echo "=========================================================="
echo "    INICIANDO REPARACIONES DE WAYLAND, WAYDROID Y OBS"
echo "=========================================================="
echo ""

# ------------------------------------------------------------------------------
# 1. REPARACIÓN WAYLAND: Instalación de xdg-desktop-portal-wlr y herramientas
# ------------------------------------------------------------------------------
echo "[1/4] Reparando componentes de Wayland y Portals para labwc/XFCE..."

echo " -> Actualizando lista de paquetes e instalando 'xdg-desktop-portal-wlr' y 'cage'..."
apt-get update -qq
apt-get install -y xdg-desktop-portal-wlr cage

# Asegurar configuración correcta de portales para labwc / XFCE
if [ -f "/usr/share/xdg-desktop-portal/xfce-portals.conf" ]; then
    echo " -> Verificada configuración en /usr/share/xdg-desktop-portal/xfce-portals.conf"
fi

# ------------------------------------------------------------------------------
# 2. REPARACIÓN WAYDROID: Corregir fallo de hook LXC (Exit code 126)
# ------------------------------------------------------------------------------
echo ""
echo "[2/4] Reparando configuración LXC de Waydroid (Error hook post-stop status 126)..."

# En config_base: cambiar post-stop = /dev/null a /bin/true
if [ -f "/usr/lib/waydroid/data/configs/config_base" ]; then
    sed -i 's|lxc.hook.post-stop = /dev/null|lxc.hook.post-stop = /bin/true|g' /usr/lib/waydroid/data/configs/config_base
    echo " -> Actualizado /usr/lib/waydroid/data/configs/config_base"
fi

# En la configuración del contenedor existente
if [ -f "/var/lib/waydroid/lxc/waydroid/config" ]; then
    sed -i 's|lxc.hook.post-stop = /dev/null|lxc.hook.post-stop = /bin/true|g' /var/lib/waydroid/lxc/waydroid/config
    echo " -> Actualizado /var/lib/waydroid/lxc/waydroid/config"
fi

# ------------------------------------------------------------------------------
# 3. REPARACIÓN WAYDROID: Ajuste GPU / Vulkan / OpenGL ES para Intel Sandy Bridge
# ------------------------------------------------------------------------------
echo ""
echo "[3/4] Ajustando propiedades gráficas de Waydroid para Intel HD Graphics 2000..."

# Intel HD 2000 (Sandy Bridge) no tiene soporte de Vulkan por hardware.
# La propiedad ro.hardware.vulkan=intel_hasvk causa fallos en la inicialización gráfica.
# Sandy Bridge soporta OpenGL ES 3.0 (196608) y no ES 3.2 (196610).

ajustar_propiedades() {
    local archivo="$1"
    if [ -f "$archivo" ]; then
        # Desactivar vulkan incompatible o dejarlo en software / none
        sed -i 's|ro.hardware.vulkan=intel_hasvk|ro.hardware.vulkan=none|g' "$archivo"
        # Ajustar GLES a 3.0 (0x00030000 = 196608)
        sed -i 's|ro.opengles.version=196610|ro.opengles.version=196608|g' "$archivo"
        echo " -> Propiedades ajustadas en $archivo"
    fi
}

ajustar_propiedades "/var/lib/waydroid/waydroid.prop"
ajustar_propiedades "/var/lib/waydroid/waydroid_base.prop"

# ------------------------------------------------------------------------------
# 4. REINICIAR SERVICIOS Y APLICAR CAMBIOS
# ------------------------------------------------------------------------------
echo ""
echo "[4/4] Reiniciando servicio de Waydroid..."
systemctl restart waydroid-container.service || true

echo ""
echo "=========================================================="
echo "          ¡REPARACIONES A NIVEL ROOT COMPLETADAS!"
echo "=========================================================="
echo ""
echo "Notas adicionales:"
echo "1. xdg-desktop-portal-wlr ha sido instalado. En la próxima sesión de Wayland"
echo "   (Xfce Wayland con labwc), OBS podrá capturar pantalla y ventanas vía PipeWire."
echo "2. Para usar Waydroid:"
echo "   - Si estás en sesión Wayland: ejecuta 'waydroid show-full-ui' (SIN sudo)."
echo "   - Si estás en sesión X11: usa 'cage -- waydroid show-full-ui' (gracias al compositor Cage instalado)."
echo "3. Para ejecutar APKs basadas en ARM (como Mario Kart Tour), instala la capa"
echo "   de traducción libndk/libhoudini usando 'waydroid-extras' o el script de Casualsnek."
echo "=========================================================="
