#!/usr/bin/env bash
#
# This script is run by Variety when a new wallpaper is set. 
# PATCHED FOR XFCE 4.20 (XUBUNTU 25.10)
#

WP=$1

detect_desktop() {
    if [ -n "$XDG_CURRENT_DESKTOP" ]; then
        case "${XDG_CURRENT_DESKTOP,,}" in
        *"gnome"*) echo "gnome" ;;
        *"unity"*) echo "unity" ;;
        *"kde"*) echo "kde" ;;
        *"xfce"*) echo "xfce" ;;
        *"lxde"*) echo "lxde" ;;
        *"lxqt"*) echo "lxqt" ;;
        *"mate"*) echo "mate" ;;
        *"cinnamon"*) echo "cinnamon" ;;
        *"lingmo"*) echo "lingmo" ;;
        *"deepin"*) echo "deepin" ;;
        *"trinity"*) echo "trinity" ;;
        *"fluxbox"*) echo "fluxbox" ;;
        *"sway"*) echo "sway" ;;
        *"enlightenment"* | *"moksha"*) echo "enlightenment" ;;
        *) echo "$XDG_CURRENT_DESKTOP" | tr '[:upper:]' '[:lower:]' ;;
        esac
        return
    fi
    echo "unknown"
}

DE=$(detect_desktop)

if [ "$DE" == "xfce" ]; then
    # XFCE Improved Patch for 4.20+
    command -v xfconf-query >/dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        # Intentar obtener propiedades existentes
        PROPS=$(xfconf-query -c xfce4-desktop -p /backdrop -l 2>/dev/null | grep -E -e "screen.*/monitor.*image-path$" -e "screen.*/monitor.*/last-image$")
        
        if [ -z "$PROPS" ]; then
            # Si no existen, las creamos dinámicamente detectando el hardware
            MONITORS=$(xrandr --query | grep " connected" | cut -d" " -f1)
            WORKSPACES=$(xfconf-query -c xfwm4 -p /general/workspace_count 2>/dev/null || echo 1)
            
            for m in $MONITORS; do
                for ((w=0; w<$WORKSPACES; w++)); do
                    xfconf-query -c xfce4-desktop -p "/backdrop/screen0/monitor$m/workspace$w/last-image" -n -t string -s "$WP" 2>/dev/null
                    xfconf-query -c xfce4-desktop -p "/backdrop/screen0/monitor$m/workspace$w/image-style" -n -t int -s 3 2>/dev/null
                done
            done
        else
            # Si ya existen, las actualizamos todas
            for i in $PROPS; do
                xfconf-query -c xfce4-desktop -p "$i" -s "$WP" 2>/dev/null
            done
        fi
        xfdesktop --reload
    fi
else
    # Si no es Xfce, podrías querer mantener el comportamiento original aquí.
    # Por ahora, solo hemos parcheado la parte necesaria para Xfce.
    echo "Desktop is $DE. For other desktops, use the original Variety script."
fi

exit 0
