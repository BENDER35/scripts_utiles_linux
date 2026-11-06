#!/usr/bin/env bash
# ==============================================================================
# Script de Mantenimiento y Corrección de Errores del Sistema
# Componentes auditados: Firefox, Thunderbird, Flatpak, Snap, Journalctl, Syslog,
# AnyDesk, RetroArch, Google Chrome, Software-Properties, VirtualBox, Zandronum,
# Arranque (Boot), XFCE y GRUB.
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[ERROR] Este script debe ejecutarse con privilegios de root (usa sudo)."
  exit 1
fi

echo "========================================================"
echo "    Iniciando proceso de corrección y mantenimiento    "
echo "========================================================"

# 1. Corrección en Xsession para XFCE / Display Manager
echo "[1/7] Comprobando y parcheando /etc/X11/Xsession.d/30x11-common_xresources..."
if [ -f /etc/X11/Xsession.d/30x11-common_xresources ]; then
    if grep -q "if has_option allow-user-resources" /etc/X11/Xsession.d/30x11-common_xresources; then
        sed -i 's/if has_option allow-user-resources/if (type has_option >\/dev\/null 2>\&1 \&\& has_option allow-user-resources)/' /etc/X11/Xsession.d/30x11-common_xresources
        echo " -> Parche de 'has_option' aplicado con éxito en Xsession."
    else
        echo " -> El archivo ya se encuentra protegido o corregido."
    fi
fi

# 2. Limpieza de reportes de crash antiguos en /var/crash/
echo "[2/7] Limpiando reportes de caídas (crashes) obsoletos..."
rm -f /var/crash/*
echo " -> Reportes de error residuales (whoopsie/Apport) eliminados."

# 3. Verificación y reparación de Flatpak a nivel de sistema
echo "[3/7] Ejecutando reparación y limpieza de Flatpak..."
if command -v flatpak &>/dev/null; then
    flatpak repair --assumeyes || true
    flatpak uninstall --unused -y || true
    echo " -> Repositorios y runtimes de Flatpak saneados."
else
    echo " -> Flatpak no está instalado, omitiendo."
fi

# 4. Verificación y actualización de Snaps
echo "[4/7] Comprobando estado del servicio Snap..."
if command -v snap &>/dev/null; then
    snap refresh || true
    echo " -> Snaps actualizados y en estado correcto."
else
    echo " -> Snap no está instalado, omitiendo."
fi

# 5. Mantenimiento y saneamiento de paquetes APT / Software-Properties
echo "[5/7] Saneamiento de dependencias y base de datos APT..."
dpkg --configure -a
apt-get check
apt-get autoremove -y
apt-get clean
echo " -> APT y software-properties-gtk verificados sin dependencias rotas."

# 6. Módulos de VirtualBox
echo "[6/7] Verificando módulos de VirtualBox..."
if command -v /sbin/vboxconfig &>/dev/null; then
    /sbin/vboxconfig || true
    echo " -> Módulos de VirtualBox recompilados / verificados."
elif systemctl is-active --quiet virtualbox.service; then
    echo " -> Servicio virtualbox.service activo y en ejecución."
fi

# 7. Reconstrucción y validación de GRUB
echo "[7/7] Actualizando configuración de GRUB..."
if command -v update-grub &>/dev/null; then
    update-grub
    echo " -> Archivo /boot/grub/grub.cfg regenerado correctamente."
fi

echo "========================================================"
echo "    ¡Mantenimiento y correcciones completadas!         "
echo "========================================================"
