#!/usr/bin/env bash
# ==============================================================================
# Script de instalación y reparación con permisos root para OpenCode AI
# ==============================================================================
set -e

echo "=== Verificando permisos de superusuario (root) ==="
if [ "$EUID" -ne 0 ]; then
  echo "[ERROR] Este script debe ejecutarse con privilegios de root (ej: sudo $0)"
  exit 1
fi

echo "[INFO] Privilegios root confirmados."

# 1. Detectar usuario que invocó sudo
REAL_USER="${SUDO_USER:-$USER}"
USER_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)
echo "[INFO] Usuario detectado: $REAL_USER (Directorio home: $USER_HOME)"

# 2. Localizar binario opencode en el entorno del usuario (NVM) o en PATH
OPENCODE_BIN=""
if [ -f "$USER_HOME/.config/nvm/versions/node/v25.9.0/bin/opencode" ]; then
  OPENCODE_BIN="$USER_HOME/.config/nvm/versions/node/v25.9.0/bin/opencode"
elif command -v opencode >/dev/null 2>&1; then
  OPENCODE_BIN=$(command -v opencode)
fi

# 3. Si existe a nivel de usuario, crear enlace simbólico en /usr/local/bin para disponibilidad global del sistema
if [ -n "$OPENCODE_BIN" ]; then
  echo "[INFO] Encontrado binario de opencode en: $OPENCODE_BIN"
  echo "[INFO] Creando/actualizando enlace simbólico en /usr/local/bin/opencode..."
  ln -sf "$OPENCODE_BIN" /usr/local/bin/opencode
  chmod 755 /usr/local/bin/opencode
  echo "[OK] Enlace simbólico creado en /usr/local/bin/opencode."
else
  echo "[WARN] No se encontró el binario en la ruta de NVM del usuario."
  echo "[INFO] Intentando instalación global directa con npm a nivel de sistema..."
  if command -v npm >/dev/null 2>&1; then
    npm install -g --allow-scripts=opencode-ai opencode-ai
    echo "[OK] Instalación global de npm completada como root."
  else
    echo "[ERROR] npm no está disponible en el PATH de root. Instale Node.js/npm a nivel de sistema primero."
    exit 1
  fi
fi

# 4. Reparar permisos de caché y directorios de npm si fuera necesario
if [ -d "$USER_HOME/.npm" ]; then
  echo "[INFO] Verificando y corrigiendo permisos de $USER_HOME/.npm para el usuario $REAL_USER..."
  chown -R "$REAL_USER":"$REAL_USER" "$USER_HOME/.npm"
  echo "[OK] Permisos corregidos en ~/.npm."
fi

echo "=============================================================================="
echo " Reparación e instalación de OpenCode AI completada exitosamente a nivel root."
echo " Verificación:"
if [ -x "/usr/local/bin/opencode" ]; then
  echo "  - Ruta global: /usr/local/bin/opencode"
fi
echo "=============================================================================="
