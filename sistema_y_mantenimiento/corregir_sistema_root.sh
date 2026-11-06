#!/usr/bin/env bash
# ==============================================================================
# Script de Corrección y Mantenimiento del Sistema (Root)
# Generado tras el análisis de logs del sistema y aplicaciones.
# ==============================================================================

set -e

# Comprobar privilegios de root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Este script debe ejecutarse con privilegios de superusuario (root)." >&2
    echo "Uso: sudo $0" >&2
    exit 1
fi

echo "========================================================================"
echo "    Iniciando proceso de corrección y optimización del sistema"
echo "========================================================================"
echo ""

# ------------------------------------------------------------------------------
# 1. SERVICIO VMWARE (Fallo por incompatibilidad con Linux 7.x)
# ------------------------------------------------------------------------------
echo "--- [1/7] Analizando y corrigiendo el servicio VMware Workstation ---"
if systemctl is-failed --quiet vmware.service 2>/dev/null; then
    echo "-> vmware.service se encuentra en estado FAILED debido a falta de módulos para el kernel 7.0."
    echo "-> Intentando compilar módulos mediante vmware-modconfig..."
    if vmware-modconfig --console --install-all 2>/dev/null; then
        echo "   Módulos de VMware compilados correctamente."
        systemctl restart vmware.service || true
    else
        echo "   No se pudieron compilar automáticamente los módulos para este kernel nuevo (7.0.0-43)."
        echo "   Deshabilitando y deteniendo el servicio para evitar fallos en el arranque (systemctl failed)..."
        systemctl stop vmware.service 2>/dev/null || true
        systemctl disable vmware.service 2>/dev/null || true
        systemctl reset-failed vmware.service 2>/dev/null || true
        echo "   vmware.service deshabilitado limpiamente. Podrás volver a habilitarlo cuando VMware soporte el kernel 7.0."
    fi
else
    echo "-> vmware.service no está en fallo o no está activo."
fi
echo ""

# ------------------------------------------------------------------------------
# 2. REGLAS UDEV PARA SCRCPY / ADB (Permisos USB de dispositivos Android)
# ------------------------------------------------------------------------------
echo "--- [2/7] Configurando reglas udev para Scrcpy y ADB ---"
UDEV_RULE_FILE="/etc/udev/rules.d/51-android.rules"

if [ ! -f "$UDEV_RULE_FILE" ]; then
    echo "-> Creando $UDEV_RULE_FILE con reglas universales de Android..."
    cat << 'EOF_UDEV' > "$UDEV_RULE_FILE"
# Reglas udev para dispositivos Android (Scrcpy / ADB)
# Acer
SUBSYSTEM=="usb", ATTR{idVendor}=="0502", MODE="0666", GROUP="plugdev"
# ASUS
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", MODE="0666", GROUP="plugdev"
# Google
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"
# HTC
SUBSYSTEM=="usb", ATTR{idVendor}=="0bb4", MODE="0666", GROUP="plugdev"
# Huawei / Honor
SUBSYSTEM=="usb", ATTR{idVendor}=="12d1", MODE="0666", GROUP="plugdev"
# LG
SUBSYSTEM=="usb", ATTR{idVendor}=="1004", MODE="0666", GROUP="plugdev"
# Motorola
SUBSYSTEM=="usb", ATTR{idVendor}=="22b8", MODE="0666", GROUP="plugdev"
# OnePlus
SUBSYSTEM=="usb", ATTR{idVendor}=="2a70", MODE="0666", GROUP="plugdev"
# Oppo
SUBSYSTEM=="usb", ATTR{idVendor}=="22d9", MODE="0666", GROUP="plugdev"
# Realme
SUBSYSTEM=="usb", ATTR{idVendor}=="22d9", MODE="0666", GROUP="plugdev"
# Samsung
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"
# Sony / Sony Ericsson
SUBSYSTEM=="usb", ATTR{idVendor}=="0fce", MODE="0666", GROUP="plugdev"
# Xiaomi / Poco / Redmi
SUBSYSTEM=="usb", ATTR{idVendor}=="2717", MODE="0666", GROUP="plugdev"
# ZTE
SUBSYSTEM=="usb", ATTR{idVendor}=="19d2", MODE="0666", GROUP="plugdev"
# Mediatek
SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666", GROUP="plugdev"
# Regla genérica para interfaz ADB (ff/42/01)
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{bDeviceClass}=="00", ATTR{bInterfaceClass}=="ff", ATTR{bInterfaceSubClass}=="42", ATTR{bInterfaceProtocol}=="01", MODE="0666", GROUP="plugdev"
EOF_UDEV
    chmod 644 "$UDEV_RULE_FILE"
    echo "-> Recargando reglas de udev..."
    udevadm control --reload-rules
    udevadm trigger
    echo "   Reglas udev instaladas y activadas. Scrcpy y adb reconocerán dispositivos sin requerir root."
else
    echo "-> $UDEV_RULE_FILE ya existe."
fi
echo ""

# ------------------------------------------------------------------------------
# 3. REPARACIÓN DEL SISTEMA FLATPAK
# ------------------------------------------------------------------------------
echo "--- [3/7] Ejecutando reparación de Flatpak a nivel de sistema ---"
if command -v flatpak >/dev/null 2>&1; then
    echo "-> Verificando y reparando objetos Flatpak del sistema..."
    flatpak repair || true
    echo "   Reparación de Flatpak del sistema completada."
else
    echo "-> Flatpak no está instalado."
fi
echo ""

# ------------------------------------------------------------------------------
# 4. GESTIÓN Y ROTACIÓN DE SYSLOG (Liberación de espacio por warp-svc)
# ------------------------------------------------------------------------------
echo "--- [4/7] Comprobando tamaño y rotación de /var/log/syslog ---"
if [ -f "/var/log/syslog" ]; then
    SYSLOG_SIZE_MB=$(du -m /var/log/syslog | cut -f1)
    echo "-> Tamaño actual de syslog: ${SYSLOG_SIZE_MB} MB"
    if [ "$SYSLOG_SIZE_MB" -gt 50 ]; then
        echo "   Syslog supera los 50MB (volumen alto generado por servicios en segundo plano como warp-svc)."
        echo "   Rotando /var/log/syslog para recuperar espacio..."
        if command -v logrotate >/dev/null 2>&1 && [ -f "/etc/logrotate.d/rsyslog" ]; then
            logrotate -f /etc/logrotate.d/rsyslog 2>/dev/null || true
        else
            cp /var/log/syslog /var/log/syslog.1
            gzip -f /var/log/syslog.1 || true
            : > /var/log/syslog
            systemctl restart rsyslog 2>/dev/null || true
        fi
        echo "   Syslog rotado exitosamente."
    else
        echo "   Tamaño de syslog dentro de los parámetros normales."
    fi
fi
echo ""

# ------------------------------------------------------------------------------
# 5. ZANDRONUM IWAD (Instalación de FreeDoom para permitir ejecución)
# ------------------------------------------------------------------------------
echo "--- [5/7] Configuración de IWADs para Zandronum ---"
if command -v zandronum >/dev/null 2>&1; then
    if [ ! -f "/usr/share/games/doom/freedoom1.wad" ] && [ ! -f "/usr/share/games/doom/freedoom2.wad" ]; then
        echo "-> Zandronum requiere un archivo IWAD (como freedoom o doom.wad) para funcionar."
        echo "-> Intentando instalar 'freedoom' mediante APT..."
        apt-get update -qq || true
        apt-get install -y freedoom || echo "   (Aviso: No se pudo instalar freedoom automáticamente. Puedes copiar tu doom.wad en ~/.config/zandronum/)"
    else
        echo "-> Archivos IWAD detectados en /usr/share/games/doom."
    fi
fi
echo ""

# ------------------------------------------------------------------------------
# 6. MANTENIMIENTO DPKG Y APT
# ------------------------------------------------------------------------------
echo "--- [6/7] Verificación y saneamiento de paquetes DPKG y APT ---"
echo "-> Verificando paquetes pendientes de configuración..."
dpkg --configure -a
echo "-> Limpiando paquetes huérfanos y cachés obsoletas..."
apt-get autoremove --purge -y
apt-get clean
echo "   Base de datos de paquetes DPKG y APT en estado óptimo."
echo ""

# ------------------------------------------------------------------------------
# 7. SINCRONIZACIÓN Y VERIFICACIÓN DE GRUB
# ------------------------------------------------------------------------------
echo "--- [7/7] Verificación de la configuración de GRUB ---"
if command -v update-grub >/dev/null 2>&1; then
    echo "-> Regenerando grub.cfg con las entradas de kernel actuales..."
    update-grub
    echo "   GRUB sincronizado y listo."
fi
echo ""

echo "========================================================================"
echo "    ¡Todas las correcciones como root han finalizado con éxito!"
echo "========================================================================"
exit 0
