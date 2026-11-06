#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación Automática de Permisos y Propiedad de Archivos
# ==============================================================================
set -e

if [ "$EUID" -ne 0 ]; then
  echo "[-] Por favor, ejecuta este script con privilegios de superusuario:"
  echo "    sudo bash $0"
  exit 1
fi

echo "[*] Iniciando corrección de permisos y propiedad para el usuario 'bender'..."

# 1. Corregir archivos críticos de configuración y caché del usuario
echo "[1/4] Restaurando propiedad en .config, .cache y .local..."
chown -R bender:bender /home/bender/.cache/dconf 2>/dev/null || true
chmod 700 /home/bender/.cache/dconf 2>/dev/null || true

chown bender:bender /home/bender/.config/mimeapps.list 2>/dev/null || true
chmod 644 /home/bender/.config/mimeapps.list 2>/dev/null || true

chown -R bender:bender /home/bender/.local/share/icons 2>/dev/null || true
chown -R bender:bender /home/bender/.local/share/applications/CiscoPacketTracer* 2>/dev/null || true

# 2. Corregir archivos y proyectos de compilación en Descargas
echo "[2/4] Restaurando propiedad en proyectos y descargas..."
chown -R bender:bender /home/bender/Descargas/scrcpy/build-auto 2>/dev/null || true
chown -R bender:bender /home/bender/Descargas/script_prueba 2>/dev/null || true
chown -R bender:bender /home/bender/Descargas/script_devol_empl_IT 2>/dev/null || true
chown -R bender:bender /home/bender/Descargas/ventoy-1.1.12 2>/dev/null || true

# 3. Corregir directorio de configuraciones de agentes IA (~/.gemini)
echo "[3/4] Asegurando permisos correctos en entorno de agentes IA..."
chown -R bender:bender /home/bender/.gemini 2>/dev/null || true
chmod 700 /home/bender/.gemini 2>/dev/null || true

# 4. Asegurar permisos estándar en directorio /tmp
echo "[4/4] Verificando permisos del directorio temporal /tmp..."
chmod 1777 /tmp

echo "=============================================================================="
echo "[+] REPARACIÓN DE PERMISOS COMPLETADA CON ÉXITO."
echo "=============================================================================="
