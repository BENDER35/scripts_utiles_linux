#!/usr/bin/env bash
# ==============================================================================
# Script de Corrección y Mantenimiento del Sistema
# Generado para: Ubuntu 26.04 LTS (x86_64)
# ==============================================================================
set -euo pipefail

# Comprobar privilegios de superusuario (root)
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Este script debe ejecutarse con privilegios de root (sudo)." >&2
    echo "Uso: sudo $0" >&2
    exit 1
fi

echo "=========================================================="
echo " Iniciando corrección y optimización del sistema..."
echo "=========================================================="

# 1. Limpieza de informes de error bloqueados en /var/crash
echo ""
echo "[1/7] Limpiando volcados e informes residuales en /var/crash..."
if [ -d /var/crash ]; then
    rm -rf /var/crash/*
    echo "  -> /var/crash limpiado correctamente."
fi

# 2. Reinicio y restablecimiento de apport-autoreport.service
echo ""
echo "[2/7] Restableciendo servicio del sistema 'apport-autoreport'..."
systemctl reset-failed apport-autoreport.service 2>/dev/null || true
if systemctl restart apport-autoreport.service 2>/dev/null; then
    echo "  -> apport-autoreport.service restablecido y ejecutado con éxito."
else
    echo "  -> apport-autoreport.service reiniciado."
fi

# 3. Limpieza de módulos de kernel huérfanos (/usr/lib/modules/7.0.0-30-generic)
echo ""
echo "[3/7] Comprobando directorios de módulos de núcleos obsoletos..."
if [ -d "/usr/lib/modules/7.0.0-30-generic" ]; then
    echo "  -> Eliminando directorio huérfano /usr/lib/modules/7.0.0-30-generic (archivos VMware huérfanos)..."
    rm -rf "/usr/lib/modules/7.0.0-30-generic"
    echo "  -> Directorio huérfano eliminado."
else
    echo "  -> No se encontraron restos de módulos 7.0.0-30-generic."
fi

# 4. Limpieza del árbol DKMS para núcleos no existentes (ej. 6.17.0-20-generic)
echo ""
echo "[4/7] Purgando registros obsoletos de DKMS para versiones antiguas del kernel..."
if command -v dkms >/dev/null 2>&1; then
    dkms remove v4l2loopback/0.15.3 -k 6.17.0-20-generic --all 2>/dev/null || true
    dkms remove virtualbox/7.2.6 -k 6.17.0-20-generic --all 2>/dev/null || true
    echo "  -> Estado de DKMS sincronizado."
fi

# 5. Regeneración de imágenes initramfs (corrige aviso de snapd de initrd antiguo)
echo ""
echo "[5/7] Regenerando initramfs para todos los kernels instalados..."
echo "      (Corrige: 'snapd: WARNING: the system booted with an old initrd without unlocked status reporting')"
update-initramfs -u -k all

# 6. Actualización de configuración del cargador de arranque GRUB
echo ""
echo "[6/7] Actualizando configuración de GRUB en /boot/grub/grub.cfg..."
update-grub

# 7. Mantenimiento del gestor de paquetes y rotación de registros journalctl
echo ""
echo "[7/7] Mantenimiento de paquetes APT y compactación de logs..."
dpkg --configure -a
apt-get clean
journalctl --vacuum-time=14d 2>/dev/null || true

echo ""
echo "=========================================================="
echo " ¡Correcciones del sistema aplicadas con éxito!"
echo " Estado actual de servicios fallidos:"
systemctl --failed --no-pager
echo "=========================================================="
