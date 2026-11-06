#!/bin/bash
# ==============================================================================
# Script de Corrección y Mantenimiento del Sistema (Ejecutar como ROOT)
# Generado automáticamente tras la auditoría exhaustiva de logs.
# ==============================================================================

set -e

# Comprobar privilegios de root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Este script debe ejecutarse como root (con sudo)." >&2
    echo "Uso: sudo bash $0" >&2
    exit 1
fi

echo "================================================================="
echo "   INICIANDO CORRECCIONES Y LIMPIEZA DEL SISTEMA"
echo "================================================================="

# 1. Limpieza de informes de fallos huérfanos en /var/crash
echo ""
echo "[1/7] Limpiando volcados de error y cuelgues huérfanos en /var/crash..."
if [ -d "/var/crash" ]; then
    rm -rf /var/crash/*
    echo "  -> /var/crash vaciado con éxito."
else
    mkdir -p /var/crash
fi

# 2. Reparación y reinicio del servicio fallido apport-autoreport
echo ""
echo "[2/7] Restableciendo servicio fallido 'apport-autoreport.service'..."
systemctl reset-failed apport-autoreport.service 2>/dev/null || true
if systemctl list-unit-files | grep -q "apport-autoreport.service"; then
    systemctl restart apport-autoreport.service 2>/dev/null || true
    echo "  -> Servicio apport-autoreport reiniciado correctamente."
fi

# 3. Truncado del log inflado de AnyDesk (/var/log/anydesk.trace)
echo ""
echo "[3/7] Truncando log saturado de AnyDesk (/var/log/anydesk.trace)..."
if [ -f "/var/log/anydesk.trace" ]; then
    > /var/log/anydesk.trace
    echo "  -> /var/log/anydesk.trace truncado a 0 bytes."
else
    echo "  -> No se encontró /var/log/anydesk.trace."
fi

# 4. Eliminación de revisiones desactivadas de paquetes Snap (libera espacio)
echo ""
echo "[4/7] Limpiando revisiones obsoletas/desactivadas de paquetes Snap..."
LANG=C snap list --all | awk '/disabled/{print $1, $3}' | while read -r snapname revision; do
    echo "  -> Eliminando snap $snapname (rev $revision)..."
    snap remove "$snapname" --revision="$revision" || true
done
# Configurar retención máxima de revisiones Snap a 2
snap set system refresh.retain=2 2>/dev/null || true
echo "  -> Política de retención de Snaps fijada a 2 revisiones."

# 5. Limpieza y reparación de Flatpak a nivel de sistema
echo ""
echo "[5/7] Verificando y reparando instalación del sistema Flatpak..."
if command -v flatpak >/dev/null 2>&1; then
    flatpak repair || true
    flatpak uninstall --unused -y || true
    echo "  -> Flatpak reparado y dependencias sin uso limpiadas."
fi

# 6. Mantenimiento del gestor de paquetes APT y limpieza de núcleos antiguos
echo ""
echo "[6/7] Limpiando paquetes huérfanos y caché de APT..."
apt-get autoremove --purge -y
apt-get clean
echo "  -> Caché y paquetes huérfanos de APT limpiados."

# 7. Verificación final de servicios del sistema
echo ""
echo "[7/7] Comprobación de unidades de systemd con fallos..."
FAILED_UNITS=$(systemctl --failed --no-legend)
if [ -z "$FAILED_UNITS" ]; then
    echo "  -> ¡Excelente! No hay servicios de systemd en estado fallido."
else
    echo "  -> Unidades aún con incidencias:"
    echo "$FAILED_UNITS"
fi

echo ""
echo "================================================================="
echo "   CORRECCIONES COMO ROOT FINALIZADAS CON ÉXITO"
echo "================================================================="
