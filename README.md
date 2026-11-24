# Scripts de Reparación y Mantenimiento del Sistema / System Repair & Maintenance Scripts

> **Ubicación / Path:** `/home/bender/Descargas/scripts_reparacion/`

---

## 🇪🇸 Descripción General (Español)

Este directorio contiene una colección organizada y modular de scripts (Bash, Python y utilidades batch) desarrollados para diagnosticar, reparar, optimizar, mantener y documentar diversos subsistemas de Linux (Ubuntu/Debian), máquinas virtuales, aplicaciones de usuario y flujos de automatización técnica.

Cada script está categorizado dentro de su correspondiente subcarpeta según su ámbito operativo o la aplicación objetivo.

### Estructura de Directorios

```text
scripts_reparacion/
├── activacion_windows/           # Utilidades de activación y scripts para entornos Windows
│   └── MAS_AIO.cmd
├── desinstalacion_software/      # Detección y purga integral de software multigestor (apt, flatpak, snap...)
│   └── eliminar_software_menores.sh
├── dpkg_apt/                     # Gestión, rescate y diagnóstico de paquetería DPKG y APT
│   ├── apt_check.py
│   └── reparar_dpkg.sh
├── engrampa/                     # Parcheo y compilación de Engrampa (soporte RAR 7.x)
│   └── reparar_engrampa_root.sh
├── guias_y_manuales/             # Generación de guías técnicas, manuales y herramientas computer vision
│   ├── samsung_n150/             # Análisis visual de puertos, vistas y guía gráfica del Samsung N150 (36 scripts)
│   ├── tcl/                      # Compilación y maquetación de guía técnica de dispositivos TCL
│   │   └── generar_manual_tcl.py
│   └── xbox_retroarch/           # Manuales ODT/DOCX y generación de activos para Xbox Retail/Dev
│       ├── build_manual_odt.py
│       ├── generar_manual_retroarch_xbox.py
│       ├── generate_bios_images.py
│       ├── generate_docx.py
│       ├── generate_error_images.py
│       ├── generate_gba_images.py
│       ├── generate_gbc_images.py
│       ├── generate_illustrations.py
│       ├── generate_n64_images.py
│       └── test_docx.py
├── memoria_swap/                 # Creación y ajuste dinámico de memoria Swap
│   └── setup_swap.sh
├── opencode/                     # Instalación y configuración de OpenCode AI
│   └── instalar_opencode_root.sh
├── pacstall/                     # Mantenimiento y saneamiento del gestor Pacstall
│   └── reparar_pacstall.sh
├── permisos/                     # Corrección de permisos de usuario ($HOME)
│   └── reparar_permisos.sh
├── pipewire_scrcpy/              # Audio PipeWire, WirePlumber y reglas udev ADB
│   └── reparar_pipewire_scrcpy.sh
├── red_y_vms/                    # Diagnóstico y reparación de redes en máquinas virtuales (VMware, VBox, KVM)
│   └── reparar_red_vms.sh
├── reportes_excel/               # Automatización, estilos y generación de hojas de cálculo e informes
│   ├── generate_all_co_sheets.py
│   ├── generate_excel_report.py
│   ├── generate_excel_report_2025.py
│   ├── generate_excel_ti_sat.py
│   ├── generate_final_co_sheets.py
│   ├── generate_sheets.py
│   ├── update_sheets.py
│   └── update_with_cv_and_ownership.py
├── retroarch/                    # Mantenimiento y logs de RetroArch (Flatpak)
│   └── reparar_retroarch.sh
├── sistema_y_mantenimiento/      # Limpieza general, GRUB, systemd, /var/crash y diagnósticos profundos
│   ├── corregir_errores_sistema.sh
│   ├── corregir_sistema_logs.sh
│   ├── corregir_sistema_root.sh
│   ├── detailed_check.py
│   ├── fix_errors.sh
│   ├── fix_system_errors.sh
│   ├── fix_system_issues.sh
│   ├── inspect_logs.py
│   ├── reparar_errores_sistema.sh
│   ├── reparar_sistema_y_logs.sh
│   ├── resolver_errores.sh
│   ├── solucionar_errores.sh
│   └── user_fixes.py
├── steam/                        # Reparación de dependencias, mandos, gráficos y Proton
│   ├── reparar_steam_dispositivos_graficos_proton_root.sh
│   └── reparar_steam_root.sh
├── variety_fondo_pantalla/       # Adaptación de fondos Variety para XFCE 4.20
│   └── set_wallpaper_parcheado.sh
├── waydroid_y_wayland/           # Contenedor Waydroid, Cage (X11) y Portales OBS
│   ├── iniciar_waydroid.sh
│   └── reparar_wayland_waydroid_obs.sh
├── .github/workflows/            # CI: espejo automático GitHub -> GitLab
│   └── mirror-gitlab.yml
├── README.md                     # Este archivo de referencia
└── GUIA_DIDACTICA.md             # Guía formativa teórica y práctica detallada
```

### Tabla Resumen de Scripts

| Categoría | Script | Privilegio / Entorno | Descripción Breve |
| :--- | :--- | :---: | :--- |
| **activacion_windows** | `MAS_AIO.cmd` | Administrador (Windows) | Script All-in-One de activación para Windows y Office (Microsoft Activation Scripts). |
| **desinstalacion_software** | `eliminar_software_menores.sh` | Root (`sudo`) | Detección y purga profunda de software infantil/educativo en apt, flatpak, snap, pacstall, brew, npm. |
| **dpkg_apt** | `apt_check.py` | Usuario / Root | Diagnóstico rápido de dependencias, repositorios PPA y conflictos en servicios APT. |
| **dpkg_apt** | `reparar_dpkg.sh` | Root (`sudo`) | Elimina bloqueos, repara dependencias y purga paquetes en estado residual (`rc`). |
| **engrampa** | `reparar_engrampa_root.sh` | Root (`sudo`) | Soluciona fallos de segmentación y soporte RAR 7.x recompilando Engrampa. |
| **guias_y_manuales** | `xbox_retroarch/*` (10 scripts) | Python 3 | Generación del manual de Xbox en ODT/DOCX, maquetación e infografías de emuladores y BIOS. |
| **guias_y_manuales** | `tcl/generar_manual_tcl.py` | Python 3 | Generación estructurada de documentación técnica para dispositivos TCL. |
| **guias_y_manuales** | `samsung_n150/*` (36 scripts) | Python 3 (PIL/NumPy) | Análisis por visión artificial de vistas, puertos e infografía técnica del netbook Samsung N150. |
| **memoria_swap** | `setup_swap.sh` | Root (`sudo`) | Calcula tamaño ideal según RAM, crea `/swapfile` y optimiza `swappiness`. |
| **opencode** | `instalar_opencode_root.sh` | Root (`sudo`) | Instala y enlaza globalmente el CLI de OpenCode AI con permisos adecuados. |
| **pacstall** | `reparar_pacstall.sh` | Root (`sudo`) | Mantenimiento, actualización de repositorios y saneamiento de Pacstall. |
| **permisos** | `reparar_permisos.sh` | Root (`sudo`) | Restaura propiedad y permisos en `.config`, `.cache` y `.local` del usuario. |
| **pipewire_scrcpy** | `reparar_pipewire_scrcpy.sh` | Root (`sudo`) | Instala `libspa-0.2-libcamera`, reglas udev Android y reinicia WirePlumber. |
| **red_y_vms** | `reparar_red_vms.sh` | Root (`sudo`) | Diagnóstico y reparación de adaptadores virtuales, NAT y puentes en VMware, VBox, KVM y Waydroid. |
| **reportes_excel** | `reportes_excel/*` (8 scripts) | Python 3 (openpyxl) | Generación y estilización automatizada de informes de control operativo, SAT y balances. |
| **retroarch** | `reparar_retroarch.sh` | Usuario | Configura rutas, repara configs y directorios de log para RetroArch Flatpak. |
| **sistema_y_mantenimiento** | `corregir_errores_sistema.sh` | Root (`sudo`) | Limpia `apport`/`/var/crash`, corrige PAM de XFCE, Postfix, Snap, Flatpak, DPKG y GRUB. |
| **sistema_y_mantenimiento** | `corregir_sistema_logs.sh` | Root (`sudo`) | Mantenimiento preventivo, corrección de logs corruptos, journald, apt y GRUB. |
| **sistema_y_mantenimiento** | `corregir_sistema_root.sh` | Root (`sudo`) | Mantenimiento integral: VMware, reglas udev, Flatpak, syslog y GRUB. |
| **sistema_y_mantenimiento** | `detailed_check.py` | Python 3 | Diagnóstico profundo del sistema: unidades systemd fallidas, volcados y paquetes rotos. |
| **sistema_y_mantenimiento** | `fix_errors.sh` | Root (`sudo`) | Regenera `/boot/grub/grubenv` para solventar errores de arranque. |
| **sistema_y_mantenimiento** | `fix_system_errors.sh` | Root (`sudo`) | Limpieza de volcados huérfanos en `/var/crash` y saneamiento de logs. |
| **sistema_y_mantenimiento** | `fix_system_issues.sh` | Root (`sudo`) | Detección de anomalías en logs y depuración de reportes del sistema. |
| **sistema_y_mantenimiento** | `inspect_logs.py` | Python 3 | Inspección selectiva y filtrado de errores críticos en `journalctl` y `syslog`. |
| **sistema_y_mantenimiento** | `reparar_errores_sistema.sh` | Root (`sudo`) | Soluciona GID `uinput`, usuarios D-Bus malcontent, systemd y paquetes. |
| **sistema_y_mantenimiento** | `reparar_sistema_y_logs.sh` | Root (`sudo`) | Corrección de fallos en Firefox, Thunderbird, Flatpak, Snap, Xsession y GRUB. |
| **sistema_y_mantenimiento** | `resolver_errores.sh` | Root (`sudo`) | Módulo DKMS Droidcam, enmascara Bluetooth ausente y deshabilita `kvm_amd`. |
| **sistema_y_mantenimiento** | `solucionar_errores.sh` | Root (`sudo`) | Resetea `recordfail` en GRUB y subsana errores críticos del sistema. |
| **sistema_y_mantenimiento** | `user_fixes.py` | Python 3 (Usuario) | Limpieza de volcados de Google Chrome y temporales huérfanos de usuario. |
| **steam** | `reparar_steam_dispositivos_graficos_proton_root.sh` | Root (`sudo`) | Instala `steam-devices` (udev mandos), backend VDPAU, variables VA-API y eleva límites `nofile` para Proton. |
| **steam** | `reparar_steam_root.sh` | Root (`sudo`) | Fuerza el Python nativo en `steamdeps` y reinstala `python3-apt` y librerías de Steam. |
| **variety_fondo_pantalla** | `set_wallpaper_parcheado.sh` | Usuario | Adapta el cambiador Variety al subsistema Xfconf de XFCE 4.20. |
| **waydroid_y_wayland** | `iniciar_waydroid.sh` | Usuario | Lanza Waydroid en Wayland nativo o encapsulado en Cage si se está en X11. |
| **waydroid_y_wayland** | `reparar_wayland_waydroid_obs.sh` | Root (`sudo`) | Instala portales WLR, compositor Cage y configura captura en OBS Studio. |

---

### 🆕 Inventario detallado de los scripts añadidos en la última actualización (v1.4.0)

El commit `5ad0760` incorporó **63 archivos nuevos** (además de actualizar esta documentación). Se listan a continuación agrupados por Finalidad para que cada script quede documentado individualmente.

#### Instalación y limpieza de software

- **`activacion_windows/MAS_AIO.cmd`** — Script All-in-One (v3.12) de Microsoft Activation Scripts para activar Windows/Office; requiere administrador en Windows.
- **`desinstalacion_software/eliminar_software_menores.sh`** — Detecta y purga software infantil, educativo y de control parental en `apt`, `flatpak`, `snap`, `npm`, `pacstall`, `pipx`, `node`, `bun` y `brew`.
- **`dpkg_apt/apt_check.py`** — Comprobación rápida de `apt-get update --dry-run`, conflictos de PPA y revisión del archivo de servicio systemd de AnyDesk.

#### Redes en máquinas virtuales

- **`red_y_vms/reparar_red_vms.sh`** — Diagnóstico y reparación de adaptadores, NAT y puentes en VMware Workstation, VirtualBox y QEMU/KVM (requiere root).

#### Guías técnicas y recursos gráficos

- **`guias_y_manuales/tcl/generar_manual_tcl.py`** — Genera el manual técnico (HTML para maquetación ODT) de root, bootloader y custom ROMs en TCL 40 SE y tablets TCL.

**Samsung N150 — obtención y análisis de material (36 scripts):**

| Script | Función |
| :--- | :--- |
| `download_check.py` | Comprueba y descarga las imágenes de referencia del netbook. |
| `download_more.py` | Descarga imágenes adicionales del Samsung N150. |
| `find_manual_pdf.py` | Busca el manual oficial en PDF mediante DuckDuckGo. |
| `parse_review.py` | Analiza el review de Notebookcheck para extraer datos. |
| `inspect_zoom.py` | Inspecciona las imágenes ampliadas del review de Notebookcheck. |
| `analyze_front.py` | Analiza en escala de grises la vista frontal. |
| `analyze_front_details.py` | Analiza detalles de color de la vista frontal. |
| `compare_views.py` | Compara la vista abierta (`open_view.jpg`) con otras vistas. |
| `find_left_ports.py` | Localiza los puertos del lateral izquierdo. |
| `find_right_ports.py` | Localiza los puertos del lateral derecho. |
| `find_switch.py` | Localiza el interruptor (switch) en la vista frontal. |
| `inspect_ports.py` | Inspección detallada del recuadro de puertos izquierdos. |
| `inspect_view_05.py` | Inspección de la vista 05 del review. |
| `inspect_view_61.py` | Inspección de la vista 61 del review. |
| `inspect_outdoor.py` | Inspección de la fotografía frontal en exterior. |
| `test_views.py` | Pruebas de coordenadas sobre las vistas generales. |
| `test_profile_views.py` | Pruebas de coordenadas sobre las vistas de perfil. |
| `test_outdoor_coords.py` | Validación de coordenadas de la imagen exterior. |
| `inspect_kb.py` | Inspección general del teclado. |
| `inspect_kb_edges.py` | Inspección de los bordes del teclado. |
| `inspect_kb_power.py` | Inspección del área de alimentación del teclado. |
| `inspect_touchpad.py` | Inspección del touchpad. |
| `inspect_cr.py` | Inspección del lector de tarjetas (card reader). |
| `inspect_detail.py` | Inspección de detalles varios de las imágenes. |
| `inspect_images.py` | Inspección rápida del conjunto de imágenes descargadas. |
| `inspect_freigestellt_quadrants.py` | Analiza por cuadrantes la imagen `freigestellt.jpg`. |
| `locate_features.py` | Localiza características destacadas en `freigestellt.jpg`. |
| `locate_freigestellt_parts.py` | Localiza piezas concretas en `freigestellt.jpg`. |
| `map_image.py` | Mapeo de coordenadas sobre `freigestellt.jpg`. |
| `map_image2.py` | Mapeo de coordenadas sobre `open_view.jpg`. |
| `map_more.py` | Mapeo ampliado de coordenadas de las vistas. |
| `generate_annotated_image.py` | Genera la imagen anotada con etiquetas y flechas. |
| `generate_infographic.py` | Genera la infografía técnica final. |
| `test_coords.py` | Valida coordenadas sobre `test_layout.jpg`. |
| `test_descriptions.py` | Comprueba cajas de texto y descripciones de las vistas. |
| `make_samsung_n150_guide.py` | Ensambla la guía gráfica completa del Samsung N150 a partir de las imágenes procesadas. |

**Xbox / RetroArch (10 scripts):**

| Script | Función |
| :--- | :--- |
| `build_manual_odt.py` | Empaqueta el manual HTML y sus activos en un ODT válido. |
| `generar_manual_retroarch_xbox.py` | Genera el manual de instalación y compatibilidad de RetroArch en Xbox Retail/Dev. |
| `generate_docx.py` | Maqueta el manual en DOCX con tablas, estilos y cabeceras. |
| `generate_illustrations.py` | Genera ilustraciones generales para el manual. |
| `generate_bios_images.py` | Genera imágenes de apoyo sobre BIOS/arranque. |
| `generate_error_images.py` | Genera capturas de errores comunes para la sección de troubleshooting. |
| `generate_gba_images.py` | Genera imágenes de compatibilidad con GBA. |
| `generate_gbc_images.py` | Genera imágenes de compatibilidad con GBC. |
| `generate_n64_images.py` | Genera imágenes de compatibilidad con Nintendo 64. |
| `test_docx.py` | Prueba rápida de que `python-docx` está disponible. |

#### Informes y hojas de cálculo (Python / openpyxl)

| Script | Función |
| :--- | :--- |
| `generate_all_co_sheets.py` | Genera todas las hojas de control operativo (CO) de una sola vez. |
| `generate_excel_report.py` | Informe Excel con gráficas de barras, líneas, tarta y anillo. |
| `generate_excel_report_2025.py` | Informe de empleo 2025 con gráficas y estilos corporativos. |
| `generate_excel_ti_sat.py` | Inventario de integradores de TI y SAT de la Comunidad de Madrid. |
| `generate_final_co_sheets.py` | Genera la versión final de las hojas CO. |
| `generate_sheets.py` | Genera libros Excel con paleta corporativa navy/slate/emerald. |
| `update_sheets.py` | Actualiza y reestiliza hojas existentes. |
| `update_with_cv_and_ownership.py` | Actualiza hojas incorporando CV y titularidad de los datos. |

#### Diagnóstico y saneamiento del sistema

- **`sistema_y_mantenimiento/corregir_sistema_logs.sh`** — Mantenimiento preventivo de logs corruptos, `journald`, APT y GRUB en Ubuntu 26.04.
- **`sistema_y_mantenimiento/detailed_check.py`** — Diagnóstico profundo: unidades systemd fallidas, volcados y paquetes rotos.
- **`sistema_y_mantenimiento/inspect_logs.py`** — Filtra errores críticos en `journalctl` y `syslog`.
- **`sistema_y_mantenimiento/user_fixes.py`** — Limpia volcados antiguos de Google Chrome y temporales huérfanos del usuario.

#### Integración continua

- **`.github/workflows/mirror-gitlab.yml`** — No es un script de reparación, pero se añadió en esta etapa: espeja ramas y etiquetas de GitHub a `git@gitlab.com:BENDER_5000/scripts_utiles_linux.git` en cada push a `main` o tag, y admite ejecución manual (`workflow_dispatch`).

---

## 🇬🇧 Overview (English)

This repository holds a structured, multi-domain suite of scripts (Bash, Python, Batch) built to troubleshoot, repair, optimize, maintain, and document Linux operating system subsystems (Ubuntu/Debian), virtual machine networks, user desktop environments, and technical automation workflows.

Each script is placed in a dedicated folder categorizing the targeted operational domain or application.

The latest update (v1.4.0) added **63 new scripts** (activation, software removal, APT checks, VM networking, 36 Samsung N150 vision utilities, TCL/Xbox manuals, 8 Excel report generators and system diagnostics). They are all documented individually in the [detailed inventory](#-inventario-detallado-de-los-scripts-añadidos-en-la-última-actualización-v140) above. Branch and tag mirroring to GitLab is handled by `.github/workflows/mirror-gitlab.yml`.

### Quick Usage Guidelines

1. **Verify executable permissions:**
   ```bash
   chmod +x /home/bender/Descargas/scripts_reparacion/*/*.sh
   ```

2. **Executing Root Scripts (Bash):**
   Scripts modifying kernel parameters, drivers, package managers, network bridges, or `/var` directories require administrative privileges:
   ```bash
   sudo bash /home/bender/Descargas/scripts_reparacion/<categoria>/<script>.sh
   ```

3. **Executing User-Space Scripts (Bash):**
   Scripts managing user configurations, Flatpak user sandboxes, or graphical sessions should **NOT** be launched with `sudo`:
   ```bash
   bash /home/bender/Descargas/scripts_reparacion/waydroid_y_wayland/iniciar_waydroid.sh
   bash /home/bender/Descargas/scripts_reparacion/retroarch/reparar_retroarch.sh
   ```

4. **Executing Python Diagnostic and Generation Utilities:**
   Run with the user interpreter (virtualenv or system python):
   ```bash
   python3 /home/bender/Descargas/scripts_reparacion/<categoria>/<script>.py
   ```

5. **Educational Guide:**
   For an in-depth breakdown of how Linux processes, memory management, virtual networks, and D-Bus interfaces operate behind each script, read [GUIA_DIDACTICA.md](GUIA_DIDACTICA.md).
