#!/usr/bin/env bash
# Script para resolver los errores detectados en los logs del sistema

echo "=========================================================="
echo "Iniciando script de resolución de errores..."
echo "=========================================================="

# 1. Compilar e instalar el módulo v4l2loopback_dc de Droidcam con DKMS
if [ -d "/home/bender/Descargas/droidcam" ]; then
    echo "[*] Compilando e instalando el módulo de kernel para Droidcam (v4l2loopback_dc) con DKMS..."
    cd /home/bender/Descargas/droidcam
    sudo ./install-dkms
else
    echo "[!] No se encontró el directorio de Droidcam en /home/bender/Descargas/droidcam. Omitiendo."
fi

# 2. Enmascarar el servicio bluetooth.service para detener el spam de activación de D-Bus
echo "[*] Enmascarando bluetooth.service (debido a falta de hardware Bluetooth)..."
sudo systemctl mask bluetooth.service

# 3. Deshabilitar completamente el intento de cargar kvm_amd en un procesador Intel
echo "[*] Deshabilitando la carga del módulo kvm_amd..."
echo "install kvm_amd /bin/true" | sudo tee /etc/modprobe.d/disable-kvm-amd.conf > /dev/null

# 4. Actualizar la configuración de GRUB
echo "[*] Actualizando GRUB..."
sudo update-grub

echo "=========================================================="
echo "¡Script de resolución de errores completado!"
echo "=========================================================="
