#!/bin/bash

# ==============================================================================
# Script de Configuración Automática de Swap para Ubuntu
# ==============================================================================
# Este script calcula de forma automática el tamaño de swap recomendado
# basándose en la memoria RAM total del sistema, crea el archivo swap de forma
# segura y lo activa de manera persistente.
# ==============================================================================

# Asegurar que el script se ejecuta como root (sudo)
if [[ $EUID -ne 0 ]]; then
   echo "[ERROR] Este script debe ejecutarse como root. Por favor, usa: sudo $0"
   exit 1
fi

echo "======================================================================"
echo "          INICIANDO CONFIGURACIÓN AUTOMÁTICA DE SWAP"
echo "======================================================================"

# 1. Obtener la memoria RAM total del sistema en Megabytes y Gigabytes
RAM_TOTAL_MB=$(free -m | awk '/^Mem:/{print $2}')
RAM_TOTAL_GB=$(echo "scale=1; $RAM_TOTAL_MB / 1024" | bc -l)
RAM_INT_GB=$(free -g | awk '/^Mem:/{print $2}')

# Si free -g devuelve 0 (sistemas con < 1GB de RAM), fijamos a 1 para los cálculos
if [ "$RAM_INT_GB" -eq 0 ]; then
    RAM_INT_GB=1
fi

echo "[*] Memoria RAM detectada: $RAM_TOTAL_MB MB (~$RAM_TOTAL_GB GB)"

# 2. Calcular el tamaño óptimo de Swap según buenas prácticas
# - Si RAM <= 2GB: Swap = 2x RAM
# - Si RAM > 2GB y <= 8GB: Swap = RAM
# - Si RAM > 8GB y <= 64GB: Swap = 4 GB (suficiente si no se requiere hibernación)
# - Si RAM > 64GB: Swap = 4 GB
if [ "$RAM_TOTAL_MB" -le 2048 ]; then
    SWAP_SIZE_MB=$((RAM_TOTAL_MB * 2))
    SWAP_SIZE_TEXT="${SWAP_SIZE_MB}M"
elif [ "$RAM_TOTAL_MB" -le 8192 ]; then
    SWAP_SIZE_MB=$RAM_TOTAL_MB
    SWAP_SIZE_TEXT="${SWAP_SIZE_MB}M"
else
    SWAP_SIZE_MB=4096
    SWAP_SIZE_TEXT="4G"
fi

echo "[*] Tamaño de Swap calculado automáticamente: $SWAP_SIZE_MB MB ($SWAP_SIZE_TEXT)"

# 3. Comprobar si ya existe swap activo
EXISTING_SWAP=$(swapon --show --noheadings | awk '{print $1}')
if [ -not -z "$EXISTING_SWAP" ]; then
    echo "[!] Se detectó swap activo en el sistema:"
    swapon --show
    echo "[*] Desactivando swap existente temporalmente para la reconfiguración..."
    swapoff -a
fi

# 4. Eliminar archivo swap antiguo si existiera en la ruta estándar
if [ -f /swapfile ]; then
    echo "[*] Eliminando archivo /swapfile antiguo..."
    rm -f /swapfile
fi

# 5. Crear el nuevo archivo swap
echo "[*] Creando el archivo swap de $SWAP_SIZE_TEXT..."
# fallocate es rápido, pero en algunos sistemas de archivos como ext4/xfs a veces da problemas 
# con el bucle de swap. Si falla, usamos 'dd'.
if ! fallocate -l "$SWAP_SIZE_TEXT" /swapfile 2>/dev/null; then
    echo "[!] fallocate falló. Intentando crear swapfile usando 'dd' (esto puede tardar unos segundos)..."
    dd if=/dev/zero of=/swapfile bs=1M count="$SWAP_SIZE_MB" status=progress
fi

# 6. Establecer los permisos de seguridad recomendados (solo root puede leer/escribir)
echo "[*] Estableciendo permisos seguros (chmod 600)..."
chmod 600 /swapfile

# 7. Formatear el archivo como espacio swap
echo "[*] Formateando el archivo como swap..."
mkswap /swapfile > /dev/null

# 8. Activar la memoria swap
echo "[*] Activando la memoria swap..."
swapon /swapfile

# 9. Hacer que el swap sea permanente tras reiniciar el sistema
echo "[*] Asegurando la persistencia en /etc/fstab..."
# Eliminar cualquier entrada previa de /swapfile en fstab para evitar duplicados
sed -i '\#^/swapfile #d' /etc/fstab

# Añadir la nueva entrada
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# 10. Mostrar el estado final del swap en el sistema
echo "======================================================================"
echo "          PROCESO DE CONFIGURACIÓN COMPLETADO"
echo "======================================================================"
swapon --show
echo ""
free -h
echo "======================================================================"
