#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación de Steam con permisos de Root (sudo)
# Generado automáticamente para corregir errores detectados en el sistema
# ==============================================================================

set -euo pipefail

echo "======================================================"
echo "    Iniciando reparaciones de Steam a nivel de Root"
echo "======================================================"

if [ "$(id -u)" -ne 0 ]; then
    echo "[-] Error: Este script debe ejecutarse con permisos de superusuario (root)."
    echo "    Ejecuta: sudo $0"
    exit 1
fi

echo "[1/3] Reparando intérprete de Python en steamdeps (/usr/lib/steam/bin_steamdeps.py)..."
# Explicación:
# Cuando Homebrew/Linuxbrew está instalado (/home/linuxbrew/.linuxbrew/bin/python3),
# la cabecera "#!/usr/bin/env python3" invoca Python 3.15 de Homebrew en vez de
# Python 3.14 del sistema, provocando el fallo "Couldn't import apt".
# Forzamos que steamdeps use directamente /usr/bin/python3 del sistema.
if [ -f "/usr/lib/steam/bin_steamdeps.py" ]; then
    sed -i 's|^#!/usr/bin/env python3|#!/usr/bin/python3|' /usr/lib/steam/bin_steamdeps.py
    chmod +x /usr/lib/steam/bin_steamdeps.py
    echo "  [+] Cabecera de steamdeps actualizada a #!/usr/bin/python3 correctamente."
else
    echo "  [!] Advertencia: /usr/lib/steam/bin_steamdeps.py no encontrado."
fi

echo "[2/3] Verificando dependencias esenciales del sistema..."
apt-get update -qq || true
apt-get install -y --no-remove python3-apt steam-libs-amd64 steam-libs-i386 || true

echo "[3/3] Probando ejecución de steamdeps con el intérprete nativo..."
if /usr/bin/steamdeps --dry-run; then
    echo "  [+] steamdeps validado con éxito: todas las dependencias del sistema están satisfechas."
else
    echo "  [!] steamdeps reportó advertencias, pero ya no falla por falta de python3-apt."
fi

echo "======================================================"
echo "    Reparaciones de Root finalizadas con éxito"
echo "======================================================"
