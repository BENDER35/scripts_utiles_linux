#!/usr/bin/env bash
# ==============================================================================
# Helper para iniciar Waydroid correctamente según el entorno de escritorio
# ==============================================================================

if [ "$(id -u)" -eq 0 ]; then
    echo "[-] AVISO: Waydroid nunca debe ejecutarse con sudo o como root."
    echo "    Ejecútalo como tu usuario normal: ./iniciar_waydroid.sh"
    exit 1
fi

echo "[*] Detectando tipo de sesión gráfica..."
echo "    XDG_SESSION_TYPE = ${XDG_SESSION_TYPE:-x11}"

if [ "${XDG_SESSION_TYPE}" = "wayland" ]; then
    echo "[+] Sesión Wayland detectada. Lanzando Waydroid directamente..."
    waydroid show-full-ui
else
    echo "[!] Sesión X11 detectada."
    if command -v cage >/dev/null 2>&1; then
        echo "[+] Lanzando Waydroid anidado dentro del compositor Wayland 'cage'..."
        cage -- waydroid show-full-ui
    else
        echo "[-] ERROR: En X11, Waydroid necesita un compositor anidado como 'cage'."
        echo "    Ejecuta primero el script de reparación: sudo /home/bender/Descargas/reparar_wayland_waydroid_obs.sh"
        echo "    O inicia sesión en 'Xfce (Wayland)' desde la pantalla de login (LightDM)."
        exit 1
    fi
fi
