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

## 🇬🇧 Overview (English)

This repository holds a structured, multi-domain suite of scripts (Bash, Python, Batch) built to troubleshoot, repair, optimize, maintain, and document Linux operating system subsystems (Ubuntu/Debian), virtual machine networks, user desktop environments, and technical automation workflows.

Each script is placed in a dedicated folder categorizing the targeted operational domain or application.

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
