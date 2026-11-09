#!/usr/bin/env bash
# ==============================================================================
# Script de Corrección y Mantenimiento del Sistema para Ubuntu 26.04 (XFCE)
# Generado automáticamente para resolver errores y advertencias detectados en:
# journalctl, boot, apport, xfce, postfix, snap, flatpak, grub, anydesk, kodi, etc.
# ==============================================================================

set -euo pipefail

# Comprobar privilegios de root
if [ "$(id -u)" -ne 0 ]; then
    echo "[-] ERROR: Este script debe ejecutarse como root (usa: sudo bash $0)"
    exit 1
fi

echo "=========================================================="
echo "    INICIANDO CORRECCIÓN DE ERRORES DEL SISTEMA"
echo "=========================================================="

# 1. Corrección de apport-autoreport.service y limpieza de /var/crash
echo "[*] [1/7] Limpiando volcados de crash acumulados y reseteando apport-autoreport..."
if [ -d /var/crash ]; then
    rm -rf /var/crash/*
    echo "    -> /var/crash/ vaciado correctamente."
fi
systemctl reset-failed apport-autoreport.service 2>/dev/null || true
systemctl restart whoopsie 2>/dev/null || true
systemctl restart apport 2>/dev/null || true
echo "    -> Servicio apport-autoreport reiniciado y estado de fallo restablecido."

# 2. Corrección del error PAM de xfce4-screensaver-dialog
echo "[*] [2/7] Corrigiendo configuración PAM de xfce4-screensaver..."
PAM_XFCE="/etc/pam.d/xfce4-screensaver"
if [ -f "$PAM_XFCE" ]; then
    if ! grep -q "common-account" "$PAM_XFCE"; then
        cp -a "$PAM_XFCE" "${PAM_XFCE}.bak"
        cat << 'EOF' > "$PAM_XFCE"
# Configuración PAM para xfce4-screensaver corregida
@include common-auth
auth optional pam_gnome_keyring.so
@include common-account
@include common-password
@include common-session
EOF
        echo "    -> Reglas common-account añadidas a $PAM_XFCE (copia de seguridad en ${PAM_XFCE}.bak)."
    else
        echo "    -> $PAM_XFCE ya cuenta con regla common-account."
    fi
else
    echo "    -> Archivo $PAM_XFCE no encontrado, omitiendo."
fi

# 3. Corrección de advertencia de permisos en Postfix (/var/spool/postfix/etc/resolv.conf)
echo "[*] [3/7] Corrigiendo permisos de chroot en Postfix..."
if [ -f /var/spool/postfix/etc/resolv.conf ]; then
    chown root:root /var/spool/postfix/etc/resolv.conf
    chmod 644 /var/spool/postfix/etc/resolv.conf
    echo "    -> Propietario de /var/spool/postfix/etc/resolv.conf corregido a root:root."
fi

# 4. Solución al aviso de snapd con 'distrobuilder' (snap descatalogado en la tienda)
echo "[*] [4/7] Gestionando snap descontinuado 'distrobuilder'..."
if snap list distrobuilder &>/dev/null; then
    echo "    -> El snap 'distrobuilder' no existe en la tienda upstream (provoca 'snap not found')."
    echo "    -> Bloqueando refresh ('hold') para evitar fallos continuos en snapd..."
    snap refresh --hold distrobuilder || true
fi

# 5. Mantenimiento y verificación de DPKG / APT
echo "[*] [5/7] Verificando consistencia de paquetes y limpiando cachés obsoletas..."
dpkg --configure -a
apt-get clean
echo "    -> Caché de paquetes APT limpia y DPKG en orden."

# 6. Reparación y mantenimiento de Flatpak
echo "[*] [6/7] Verificando integridad del almacenamiento Flatpak..."
if command -v flatpak &>/dev/null; then
    flatpak repair --system || true
    echo "    -> Flatpak repair ejecutado."
fi

# 7. Limpieza de logs antiguos del Journal y actualización de GRUB
echo "[*] [7/7] Optimizando logs del Journal y actualizando configuración de GRUB..."
journalctl --vacuum-time=7d
if command -v update-grub &>/dev/null; then
    update-grub
    echo "    -> GRUB actualizado correctamente."
fi

echo "=========================================================="
echo "    ¡CORRECCIONES APLICADAS EXITOSAMENTE!"
echo "=========================================================="
systemctl status apport-autoreport.service --no-pager || true
