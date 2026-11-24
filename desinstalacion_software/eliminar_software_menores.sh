#!/usr/bin/env bash
# ==============================================================================
# Script de detección y desinstalación completa de software para menores /
# ocio / educativo / control parental en Linux.
# Compatible con: apt, flatpak, snap, npm, pacstall, pipx, node, bun y brew.
# ==============================================================================

set -uo pipefail

# Colores para salida de terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # Sin color

echo -e "${BOLD}${CYAN}================================================================${NC}"
echo -e "${BOLD}${CYAN}   Gestor de Detección y Borrado Completo de Software Menores   ${NC}"
echo -e "${BOLD}${CYAN}================================================================${NC}\n"

# Arrays para almacenar elementos detectados: formato "GESTOR|ID_PAQUETE|DESCRIPCION"
DETECTED_ITEMS=()

check_manager() {
    command -v "$1" >/dev/null 2>&1
}

# Generar el comando de borrado completo para un gestor y paquete dado
get_purge_command() {
    local manager="$1"
    local pkg="$2"
    case "$manager" in
        APT)
            echo "sudo apt purge --autoremove -y $pkg && sudo apt clean"
            ;;
        FLATPAK)
            echo "flatpak uninstall --delete-data -y $pkg"
            ;;
        SNAP)
            echo "sudo snap remove --purge $pkg"
            ;;
        PACSTALL)
            echo "pacstall -R $pkg"
            ;;
        PIPX)
            echo "pipx uninstall $pkg"
            ;;
        NPM|NODE)
            echo "npm uninstall -g $pkg"
            ;;
        BUN)
            echo "bun remove -g $pkg"
            ;;
        BREW)
            echo "brew uninstall --force --zap $pkg 2>/dev/null || brew uninstall --force $pkg; brew cleanup -s $pkg"
            ;;
        *)
            echo "# Comando desconocido para $manager"
            ;;
    esac
}

echo -e "${YELLOW}[*] Escaneando gestores de paquetes en el sistema...${NC}\n"

# ------------------------------------------------------------------------------
# 1. FLATPAK
# ------------------------------------------------------------------------------
if check_manager flatpak; then
    FLATPAK_KIDS_PATTERNS=(
        "net.supertuxkart.SuperTuxKart:SuperTuxKart (Juego de carreras arcade apto para menores)"
        "org.supertuxproject.SuperTux:SuperTux (Juego de plataformas estilo Mario clásico)"
        "net.sourceforge.ExtremeTuxRacer:Extreme Tux Racer (Juego de carreras árticas)"
        "com.voxdsp.TuxVsDragon:Tux VS Dragon (Minijuego con Tux)"
        "net.sourceforge.Klavaro:Klavaro (Tutor de mecanografía escolar)"
        "org.kde.kolourpaint:KolourPaint (Herramienta básica de dibujo)"
        "org.sonic3air.Sonic3AIR:Sonic 3: A.I.R (Juego clásico de plataformas infantil/juvenil)"
        "org.kartkrew.RingRacers:Dr. Robotnik's Ring Racers (Juego de karts de Sonic)"
        "org.hedgewars.Hedgewars:Hedgewars (Juego por turnos cómico estilo Worms)"
        "org.gnome.Aisleriot:Solitario Aisleriot (Juegos de cartas clásicos)"
        "org.kde.ksudoku:KSudoku (Rompecabezas de Sudoku)"
        "com.github.k4zmu2a.spacecadetpinball:Space Cadet Pinball (Juego Pinball clásico)"
        "org.kde.gcompris:GCompris (Suite educativa para niños de 2 a 10 años)"
        "org.tuxpaint.Tuxpaint:Tux Paint (Programa de dibujo para niños)"
        "edu.mit.Scratch:Scratch (Entorno de programación visual para niños)"
        "org.kde.kturtle:KTurtle (Entorno educativo de programación con tortuga)"
    )

    INSTALLED_FLATPAKS=$(flatpak list --app --columns=application 2>/dev/null || true)
    for entry in "${FLATPAK_KIDS_PATTERNS[@]}"; do
        app_id="${entry%%:*}"
        app_desc="${entry#*:}"
        if echo "$INSTALLED_FLATPAKS" | grep -qx "$app_id"; then
            DETECTED_ITEMS+=("FLATPAK|$app_id|$app_desc")
        fi
    done
fi

# ------------------------------------------------------------------------------
# 2. APT (Debian/Ubuntu)
# ------------------------------------------------------------------------------
if check_manager apt; then
    APT_KIDS_PATTERNS=(
        "sgt-puzzles:Simon Tatham's Puzzles (Colección de rompecabezas lógicos)"
        "sgt-launcher:Lanzador para la colección sgt-puzzles"
        "gnome-mines:Buscaminas de GNOME"
        "gnome-sudoku:Sudoku de GNOME"
        "drascula:Aventura gráfica Drascula: The Vampire Strikes Back"
        "drascula-music:Archivos de audio de Drascula"
        "drascula-spanish:Versión en español de Drascula"
        "visualboyadvance:Emulador de Game Boy Advance"
        "gcompris:Suite educativa completa para niños de 2 a 10 años"
        "gcompris-qt:Suite educativa para niños (versión Qt)"
        "tuxpaint:Programa de dibujo para niños pequeños"
        "tuxmath:Juego educativo de matemáticas con Tux"
        "tuxtype:Tutor de mecanografía para niños con Tux"
        "scratch:Lenguaje de programación visual educativo"
        "kturtle:Entorno educativo de programación"
        "childsplay:Juegos educativos para niños pequeños"
        "timekpr-next:Software de control parental de tiempo de uso"
        "malcontent-gui:Interfaz de control parental de GNOME"
    )

    for entry in "${APT_KIDS_PATTERNS[@]}"; do
        pkg_name="${entry%%:*}"
        pkg_desc="${entry#*:}"
        if dpkg -s "$pkg_name" 2>/dev/null | grep -q "Status: install ok installed"; then
            DETECTED_ITEMS+=("APT|$pkg_name|$pkg_desc")
        fi
    done
fi

# ------------------------------------------------------------------------------
# 3. SNAP
# ------------------------------------------------------------------------------
if check_manager snap; then
    SNAP_KIDS_PATTERNS=(
        "supertuxkart:SuperTuxKart"
        "supertux:SuperTux"
        "tuxpaint:Tux Paint"
        "scratch:Scratch Desktop"
        "gcompris:GCompris"
    )
    INSTALLED_SNAPS=$(snap list 2>/dev/null | awk 'NR>1 {print $1}' || true)
    for entry in "${SNAP_KIDS_PATTERNS[@]}"; do
        pkg_name="${entry%%:*}"
        pkg_desc="${entry#*:}"
        if echo "$INSTALLED_SNAPS" | grep -qx "$pkg_name"; then
            DETECTED_ITEMS+=("SNAP|$pkg_name|$pkg_desc")
        fi
    done
fi

# ------------------------------------------------------------------------------
# 4. PACSTALL
# ------------------------------------------------------------------------------
if check_manager pacstall; then
    INSTALLED_PACSTALL=$(pacstall -L 2>/dev/null | grep '^~' | awk '{print $2}' | cut -d'@' -f1 || true)
    PACSTALL_PATTERNS=("scratch" "tuxpaint" "gcompris" "supertux")
    for pat in "${PACSTALL_PATTERNS[@]}"; do
        if echo "$INSTALLED_PACSTALL" | grep -qi "^$pat$"; then
            DETECTED_ITEMS+=("PACSTALL|$pat|Paquete pacstall de ocio/educativo")
        fi
    done
fi

# ------------------------------------------------------------------------------
# 5. PIPX
# ------------------------------------------------------------------------------
if check_manager pipx; then
    INSTALLED_PIPX=$(pipx list --short 2>/dev/null | awk '{print $1}' || true)
fi

# ------------------------------------------------------------------------------
# 6. NPM / NODE GLOBAL
# ------------------------------------------------------------------------------
if check_manager npm; then
    INSTALLED_NPM=$(npm list -g --depth=0 --json 2>/dev/null || true)
fi

# ------------------------------------------------------------------------------
# 7. BUN GLOBAL
# ------------------------------------------------------------------------------
if check_manager bun; then
    :
fi

# ------------------------------------------------------------------------------
# 8. HOMEBREW (BREW)
# ------------------------------------------------------------------------------
if check_manager brew; then
    :
fi

# ==============================================================================
# MOSTRAR RESULTADOS DETECTADOS
# ==============================================================================
TOTAL_ITEMS=${#DETECTED_ITEMS[@]}

if [ "$TOTAL_ITEMS" -eq 0 ]; then
    echo -e "${GREEN}[✔] No se detectó software infantil, educativo ni de control parental en el sistema.${NC}"
    exit 0
fi

echo -e "${BOLD}Se han detectado los siguientes ${TOTAL_ITEMS} paquetes para menores / ocio / educación:${NC}\n"

for i in "${!DETECTED_ITEMS[@]}"; do
    IFS='|' read -r manager pkg desc <<< "${DETECTED_ITEMS[$i]}"
    idx=$((i + 1))
    printf "  ${BOLD}%2d)${NC} [${BLUE}%-7s${NC}] ${GREEN}%-35s${NC} - %s\n" "$idx" "$manager" "$pkg" "$desc"
done

echo ""
echo -e "${YELLOW}NOTA IMPORTANTE DE SEGURIDAD:${NC}"
echo -e "  - La librería ${BOLD}libmalcontent-0-0${NC} (control parental de GNOME) NO se incluye en esta lista"
echo -e "    porque es una dependencia crítica del paquete ${BOLD}flatpak${NC} en el sistema. Borrarla rompería Flatpak."
echo ""

# ==============================================================================
# GUÍA RÁPIDA DE COMANDOS DE BORRADO COMPLETO POR GESTOR
# ==============================================================================
show_reference_commands() {
    echo -e "\n${BOLD}${CYAN}================================================================${NC}"
    echo -e "${BOLD}${CYAN}   GUÍA: Comandos de borrado completo para cada gestor          ${NC}"
    echo -e "${BOLD}${CYAN}================================================================${NC}"
    echo -e "${BOLD}1. APT (requiere root):${NC}"
    echo -e "   ${GREEN}sudo apt purge --autoremove -y <paquete>${NC}"
    echo -e "   ${CYAN}# Borra binarios, dependencias no usadas y archivos de configuración en /etc${NC}"
    echo -e "   ${GREEN}sudo apt clean${NC}  ${CYAN}# Limpia la caché de paquetes descargados${NC}\n"

    echo -e "${BOLD}2. FLATPAK (sin root):${NC}"
    echo -e "   ${GREEN}flatpak uninstall --delete-data -y <ID_aplicación>${NC}"
    echo -e "   ${CYAN}# Desinstala la app y BORRA todos sus datos y partidas en ~/.var/app/<ID>${NC}"
    echo -e "   ${GREEN}flatpak uninstall --unused -y${NC}  ${CYAN}# Elimina runtimes huérfanos${NC}\n"

    echo -e "${BOLD}3. SNAP (requiere root):${NC}"
    echo -e "   ${GREEN}sudo snap remove --purge <nombre_snap>${NC}"
    echo -e "   ${CYAN}# Elimina el snap SIN generar instantáneas (snapshots) ni copias de datos${NC}\n"

    echo -e "${BOLD}4. PACSTALL (requiere root si el script de instalación lo necesitó):${NC}"
    echo -e "   ${GREEN}pacstall -R <paquete>${NC}"
    echo -e "   ${CYAN}# Desinstala y limpia el paquete compilado por pacstall${NC}\n"

    echo -e "${BOLD}5. PIPX (nivel de usuario, no usar root):${NC}"
    echo -e "   ${GREEN}pipx uninstall <paquete>${NC}"
    echo -e "   ${CYAN}# Elimina el entorno virtual aislado y sus enlaces simbólicos en ~/.local/bin${NC}\n"

    echo -e "${BOLD}6. NPM / NODE (global):${NC}"
    echo -e "   ${GREEN}npm uninstall -g <paquete>${NC}  ${CYAN}# (O anteponer sudo si está en /usr/local)${NC}"
    echo -e "   ${GREEN}npm cache clean --force${NC}\n"

    echo -e "${BOLD}7. BUN (nivel de usuario, no usar root):${NC}"
    echo -e "   ${GREEN}bun remove -g <paquete>${NC}\n"

    echo -e "${BOLD}8. HOMEBREW (nivel de usuario, ¡nunca usar sudo con brew!):${NC}"
    echo -e "   ${GREEN}brew uninstall --force --zap <paquete>${NC}"
    echo -e "   ${CYAN}# --zap elimina archivos de configuración y datos asociados${NC}"
    echo -e "   ${GREEN}brew cleanup -s <paquete>${NC}  ${CYAN}# Limpia la caché de la descarga${NC}"
    echo -e "${BOLD}${CYAN}================================================================${NC}\n"
}

# Mostrar todos los comandos exactos para los elementos detectados
show_detected_commands() {
    echo -e "\n${BOLD}${CYAN}================================================================${NC}"
    echo -e "${BOLD}${CYAN}   Comandos exactos de borrado completo para copiar y pegar:    ${NC}"
    echo -e "${BOLD}${CYAN}================================================================${NC}\n"

    local apt_pkgs=()
    local flatpak_pkgs=()

    for entry in "${DETECTED_ITEMS[@]}"; do
        IFS='|' read -r manager pkg desc <<< "$entry"
        case "$manager" in
            APT) apt_pkgs+=("$pkg") ;;
            FLATPAK) flatpak_pkgs+=("$pkg") ;;
            *)
                echo -e "# [$manager] $desc"
                get_purge_command "$manager" "$pkg"
                echo ""
                ;;
        esac
    done

    if [ ${#flatpak_pkgs[@]} -gt 0 ]; then
        echo -e "# [FLATPAK] Borrado completo de aplicaciones y sus carpetas de datos (~/.var/app/):"
        for fp in "${flatpak_pkgs[@]}"; do
            echo "flatpak uninstall --delete-data -y $fp"
        done
        echo "flatpak uninstall --unused -y"
        echo ""
    fi

    if [ ${#apt_pkgs[@]} -gt 0 ]; then
        echo -e "# [APT] Borrado completo con purga de configuraciones y dependencias:"
        echo "sudo apt purge --autoremove -y ${apt_pkgs[*]}"
        echo "sudo apt clean"
        echo ""
    fi
}

# Exportar todos los elementos y comandos a un archivo de texto
export_to_txt() {
    local outfile="${1:-/home/bender/Descargas/elementos_eliminacion.txt}"
    echo -e "${YELLOW}[*] Generando archivo: $outfile ...${NC}"

    {
        echo "================================================================================"
        echo "ELEMENTOS DETECTADOS PARA MENORES / EDUCACIÓN / OCIO Y COMANDOS DE BORRADO"
        echo "Generado el: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Ruta: $outfile"
        echo "================================================================================"
        echo ""
        echo "--------------------------------------------------------------------------------"
        echo "1. LISTA DE ELEMENTOS DETECTADOS ($TOTAL_ITEMS)"
        echo "--------------------------------------------------------------------------------"
        for i in "${!DETECTED_ITEMS[@]}"; do
            IFS='|' read -r m p d <<< "${DETECTED_ITEMS[$i]}"
            printf "%2d) [%-7s] %-35s - %s\n" "$((i + 1))" "$m" "$p" "$d"
        done
        echo ""
        echo "--------------------------------------------------------------------------------"
        echo "2. COMANDOS DE BORRADO COMPLETO LISTOS PARA EJECUTAR"
        echo "--------------------------------------------------------------------------------"
        
        local apt_list=()
        local flatpak_list=()
        for entry in "${DETECTED_ITEMS[@]}"; do
            IFS='|' read -r m p d <<< "$entry"
            case "$m" in
                APT) apt_list+=("$p") ;;
                FLATPAK) flatpak_list+=("$p") ;;
                *)
                    echo "# [$m] $d"
                    get_purge_command "$m" "$p"
                    echo ""
                    ;;
            esac
        done

        if [ ${#flatpak_list[@]} -gt 0 ]; then
            echo "# [FLATPAK] Borrado completo (aplicaciones y carpetas de datos en ~/.var/app/):"
            echo "flatpak uninstall --delete-data -y \\"
            for ((j=0; j<${#flatpak_list[@]}; j++)); do
                if [ $j -eq $((${#flatpak_list[@]} - 1)) ]; then
                    echo "  ${flatpak_list[$j]}"
                else
                    echo "  ${flatpak_list[$j]} \\"
                fi
            done
            echo ""
            echo "flatpak uninstall --unused -y"
            echo ""
        fi

        if [ ${#apt_list[@]} -gt 0 ]; then
            echo "# [APT] Purga completa de paquetes, configuraciones y dependencias (requiere sudo):"
            echo "sudo apt purge --autoremove -y \\"
            for ((j=0; j<${#apt_list[@]}; j++)); do
                if [ $j -eq $((${#apt_list[@]} - 1)) ]; then
                    echo "  ${apt_list[$j]}"
                else
                    echo "  ${apt_list[$j]} \\"
                fi
            done
            echo ""
            echo "sudo apt clean"
            echo ""
        fi

        echo "--------------------------------------------------------------------------------"
        echo "3. GUÍA GENERAL DE COMANDOS DE BORRADO COMPLETO"
        echo "--------------------------------------------------------------------------------"
        echo "- APT:      sudo apt purge --autoremove -y <paquete> && sudo apt clean"
        echo "- FLATPAK:  flatpak uninstall --delete-data -y <app> && flatpak uninstall --unused -y"
        echo "- SNAP:     sudo snap remove --purge <snap>"
        echo "- PACSTALL: pacstall -R <paquete>"
        echo "- PIPX:     pipx uninstall <paquete>"
        echo "- NPM:      npm uninstall -g <paquete> && npm cache clean --force"
        echo "- BUN:      bun remove -g <paquete>"
        echo "- BREW:     brew uninstall --force --zap <paquete> && brew cleanup -s <paquete>"
        echo ""
        echo "--------------------------------------------------------------------------------"
        echo "4. ADVERTENCIA"
        echo "--------------------------------------------------------------------------------"
        echo "No eliminar 'libmalcontent-0-0' porque es dependencia de 'flatpak'."
        echo "================================================================================"
    } > "$outfile"

    echo -e "${GREEN}[✔] Archivo guardado correctamente en: ${BOLD}$outfile${NC}"
}

# ==============================================================================
# MENU DE ACCION
# ==============================================================================
echo -e "${BOLD}Opciones disponibles:${NC}"
echo -e "  [A] Desinstalar TODOS los elementos detectados con borrado completo"
echo -e "  [S] Seleccionar números específicos para desinstalar (ejemplo: 1 3 5)"
echo -e "  [C] Ver los COMANDOS exactos de borrado completo (para copiarlos tú mismo)"
echo -e "  [E] Guardar elementos y comandos en un archivo de texto (.txt)"
echo -e "  [G] Ver GUÍA de comandos de borrado completo para todos los gestores"
echo -e "  [Q] Cancelar y salir"
echo ""
read -rp "Seleccione una opción [A/S/C/E/G/Q]: " user_choice

SELECTED_INDICES=()

case "${user_choice^^}" in
    A)
        for i in "${!DETECTED_ITEMS[@]}"; do
            SELECTED_INDICES+=("$i")
        done
        ;;
    S)
        echo ""
        read -rp "Indique los números separados por espacio: " -a num_choices
        for num in "${num_choices[@]}"; do
            if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le "$TOTAL_ITEMS" ]; then
                SELECTED_INDICES+=("$((num - 1))")
            else
                echo -e "${RED}[!] Número no válido ignorado: $num${NC}"
            fi
        done
        ;;
    C)
        show_detected_commands
        exit 0
        ;;
    E)
        export_to_txt "/home/bender/Descargas/elementos_eliminacion.txt"
        exit 0
        ;;
    G)
        show_reference_commands
        exit 0
        ;;
    Q|*)
        echo -e "${YELLOW}Operación cancelada por el usuario.${NC}"
        exit 0
        ;;
esac

if [ ${#SELECTED_INDICES[@]} -eq 0 ]; then
    echo -e "${YELLOW}No se seleccionó ningún elemento válido. Saliendo.${NC}"
    exit 0
fi

# Confirmación final mostrando el comando exacto que se ejecutará
echo ""
echo -e "${BOLD}${RED}Comandos de borrado completo que se van a ejecutar:${NC}"
for idx in "${SELECTED_INDICES[@]}"; do
    IFS='|' read -r manager pkg desc <<< "${DETECTED_ITEMS[$idx]}"
    echo -e "  ${BOLD}[$manager]${NC} $pkg"
    echo -e "    ${MAGENTA}➔ $(get_purge_command "$manager" "$pkg")${NC}"
done

echo ""
read -rp "¿Está seguro de ejecutar estos comandos de borrado completo? (s/N): " confirm
if [[ ! "$confirm" =~ ^[sS]$ ]]; then
    echo -e "${YELLOW}Operación cancelada.${NC}"
    exit 0
fi

echo ""

# Agrupar paquetes por gestor para optimizar la desinstalación
APT_TO_REMOVE=()
FLATPAK_TO_REMOVE=()
SNAP_TO_REMOVE=()
PACSTALL_TO_REMOVE=()
PIPX_TO_REMOVE=()
NPM_TO_REMOVE=()
BREW_TO_REMOVE=()

for idx in "${SELECTED_INDICES[@]}"; do
    IFS='|' read -r manager pkg desc <<< "${DETECTED_ITEMS[$idx]}"
    case "$manager" in
        APT) APT_TO_REMOVE+=("$pkg") ;;
        FLATPAK) FLATPAK_TO_REMOVE+=("$pkg") ;;
        SNAP) SNAP_TO_REMOVE+=("$pkg") ;;
        PACSTALL) PACSTALL_TO_REMOVE+=("$pkg") ;;
        PIPX) PIPX_TO_REMOVE+=("$pkg") ;;
        NPM) NPM_TO_REMOVE+=("$pkg") ;;
        BREW) BREW_TO_REMOVE+=("$pkg") ;;
    esac
done

# ----------------- DESINSTALACIÓN FLATPAK -----------------
# Borrado completo: --delete-data borra las carpetas de datos de ~/.var/app/
# y luego --unused limpia dependencias de runtime que hayan quedado huérfanas
if [ ${#FLATPAK_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "${BOLD}${BLUE}=== Desinstalando de Flatpak (Borrado completo + eliminación de datos) ===${NC}"
    for app in "${FLATPAK_TO_REMOVE[@]}"; do
        echo -e "${CYAN}Ejecutando: flatpak uninstall --delete-data -y $app${NC}"
        flatpak uninstall --delete-data -y "$app" || true
    done
    echo -e "${CYAN}Ejecutando: flatpak uninstall --unused -y (limpiando runtimes no usados)...${NC}"
    flatpak uninstall --unused -y || true
fi

# ----------------- DESINSTALACIÓN APT -----------------
# Borrado completo: purge elimina archivos de configuración en /etc,
# autoremove --purge elimina dependencias y configs residuales, y clean vacía la caché
if [ ${#APT_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "\n${BOLD}${BLUE}=== Desinstalando de APT (Borrado completo con purga de configuraciones - requiere sudo) ===${NC}"
    echo -e "${CYAN}Ejecutando: sudo apt purge -y ${APT_TO_REMOVE[*]}${NC}"
    sudo apt purge -y "${APT_TO_REMOVE[@]}" || true

    echo -e "${CYAN}Ejecutando: sudo apt autoremove --purge -y (limpiando dependencias y configuraciones residuales)...${NC}"
    sudo apt autoremove --purge -y || true

    echo -e "${CYAN}Ejecutando: sudo apt clean (limpiando caché de paquetes)...${NC}"
    sudo apt clean || true
fi

# ----------------- DESINSTALACIÓN SNAP -----------------
# Borrado completo: --purge evita que snap guarde instantáneas (snapshots de copia de seguridad)
if [ ${#SNAP_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "\n${BOLD}${BLUE}=== Desinstalando de Snap (Borrado completo sin guardar snapshots - requiere sudo) ===${NC}"
    for sn in "${SNAP_TO_REMOVE[@]}"; do
        echo -e "${CYAN}Ejecutando: sudo snap remove --purge $sn${NC}"
        sudo snap remove --purge "$sn" || true
    done
fi

# ----------------- DESINSTALACIÓN PACSTALL -----------------
if [ ${#PACSTALL_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "\n${BOLD}${BLUE}=== Desinstalando de Pacstall (Borrado completo) ===${NC}"
    for pac in "${PACSTALL_TO_REMOVE[@]}"; do
        echo -e "${CYAN}Ejecutando: pacstall -R $pac${NC}"
        pacstall -R "$pac" || true
    done
fi

# ----------------- DESINSTALACIÓN PIPX -----------------
# pipx uninstall elimina el virtualenv y todos los symlinks en ~/.local/bin
if [ ${#PIPX_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "\n${BOLD}${BLUE}=== Desinstalando de Pipx (Borrado completo de venv y binarios) ===${NC}"
    for px in "${PIPX_TO_REMOVE[@]}"; do
        echo -e "${CYAN}Ejecutando: pipx uninstall $px${NC}"
        pipx uninstall "$px" || true
    done
fi

# ----------------- DESINSTALACIÓN NPM -----------------
if [ ${#NPM_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "\n${BOLD}${BLUE}=== Desinstalando de NPM global ===${NC}"
    for np in "${NPM_TO_REMOVE[@]}"; do
        echo -e "${CYAN}Ejecutando: npm uninstall -g $np${NC}"
        npm uninstall -g "$np" || sudo npm uninstall -g "$np" || true
    done
    echo -e "${CYAN}Ejecutando: npm cache clean --force${NC}"
    npm cache clean --force || true
fi

# ----------------- DESINSTALACIÓN BREW -----------------
# Borrado completo: --force y --zap eliminan fórmulas/casks y configuraciones, más cleanup
if [ ${#BREW_TO_REMOVE[@]} -gt 0 ]; then
    echo -e "\n${BOLD}${BLUE}=== Desinstalando de Homebrew (Borrado completo y limpieza de caché) ===${NC}"
    for bw in "${BREW_TO_REMOVE[@]}"; do
        echo -e "${CYAN}Ejecutando: brew uninstall --force --zap $bw${NC}"
        brew uninstall --force --zap "$bw" 2>/dev/null || brew uninstall --force "$bw" || true
        echo -e "${CYAN}Ejecutando: brew cleanup -s $bw${NC}"
        brew cleanup -s "$bw" || true
    done
fi

echo -e "\n${BOLD}${GREEN}[✔] ¡Proceso de borrado completo finalizado con éxito!${NC}"
