#!/usr/bin/env bash
# Script para solucionar automáticamente los errores de logs del sistema
# Debe ejecutarse con privilegios de superusuario (sudo)

# Asegurar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
  echo "[-] Por favor, ejecuta este script usando sudo: sudo bash $0"
  exit 1
fi

echo "============================================================"
echo "   INICIANDO REPARACIÓN DE ERRORES DETECTADOS EN EL SISTEMA"
echo "============================================================"
echo

# 1. Reparación del bloque de entorno de GRUB
echo "--- [1/4] Reparando bloque de entorno de GRUB ---"
if [ -f /boot/grub/grubenv ]; then
    echo "[*] Recreando un bloque de entorno limpio en /boot/grub/grubenv..."
    grub-editenv /boot/grub/grubenv create
    grub-editenv /boot/grub/grubenv set recordfail=0
    echo "[+] Archivo grubenv regenerado correctamente."
else
    echo "[-] No se encontró el archivo /boot/grub/grubenv. Omitiendo."
fi
echo

# 2. Desactivar el módulo KVM de AMD en procesador Intel
echo "--- [2/4] Deshabilitando módulo KVM AMD (Procesador Intel detectado) ---"
CONF_FILE="/etc/modprobe.d/blacklist-kvm.conf"
if [ ! -f "$CONF_FILE" ] || ! grep -q "blacklist kvm_amd" "$CONF_FILE"; then
    echo "[*] Añadiendo kvm_amd a la lista negra en $CONF_FILE..."
    echo "# Deshabilitar módulo KVM AMD redundante en procesador Intel" > "$CONF_FILE"
    echo "blacklist kvm_amd" >> "$CONF_FILE"
    echo "[+] Módulo kvm_amd deshabilitado para futuros arranques."
else
    echo "[+] El módulo kvm_amd ya se encuentra en la lista negra."
fi
echo

# 3. Reparación del Snap corrupto (snapd-desktop-integration)
echo "--- [3/4] Reinstalando Snap corrupto (snapd-desktop-integration) ---"
if snap list | grep -q "snapd-desktop-integration"; then
    echo "[*] Eliminando versión corrupta de snapd-desktop-integration..."
    snap remove --purge snapd-desktop-integration
    echo "[*] Reinstalando una copia limpia de snapd-desktop-integration..."
    snap install snapd-desktop-integration
    echo "[+] Snap reinstalado con éxito."
else
    echo "[-] El snap snapd-desktop-integration no está en la lista. Omitiendo."
fi
echo

# 4. Desactivación persistente del lector de tarjetas USB defectuoso (Realtek 0bda:0151)
echo "--- [4/4] Desactivando persistentemente el lector de tarjetas USB defectuoso ---"
UDEV_FILE="/etc/udev/rules.d/99-disable-faulty-reader.rules"
echo "[*] Creando regla udev en $UDEV_FILE..."
echo "# Deshabilitar lector de tarjetas Realtek defectuoso (0bda:0151) para evitar inundacion de logs" > "$UDEV_FILE"
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="0151", ATTR{authorized}="0"' >> "$UDEV_FILE"
echo "[*] Recargando reglas de udev..."
udevadm control --reload-rules
udevadm trigger
echo "[+] Lector de tarjetas defectuoso desactivado. Se detendrá la inundación de logs."
echo

echo "============================================================"
echo "    PROCESO COMPLETADO. POR FAVOR REINICIA PARA COMPROBAR"
echo "============================================================"
