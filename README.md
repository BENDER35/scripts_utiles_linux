# Scripts de Reparación y Mantenimiento del Sistema / System Repair & Maintenance Scripts

> **Ubicación / Path:** `/home/bender/Descargas/scripts_reparacion/`

---

## 🇪🇸 Descripción General (Español)

Este directorio contiene una colección organizada de scripts en Bash desarrollados para diagnosticar, reparar, optimizar y mantener diversos subsistemas de Linux (Ubuntu/Debian) y aplicaciones de usuario.

Cada script está categorizado dentro de su propia subcarpeta según el área del sistema o la aplicación objetivo.

### Estructura de Directorios

```text
scripts_reparacion/
├── dpkg_apt/                     # Gestión y rescate de paquetería DPKG y APT
│   └── reparar_dpkg.sh
├── engrampa/                     # Parcheo y compilación de Engrampa (RAR 7.x)
│   └── reparar_engrampa_root.sh
├── memoria_swap/                 # Creación y ajuste dinámico de memoria Swap
│   └── setup_swap.sh
├── opencode/                     # Instalación y configuración de OpenCode AI
│   └── instalar_opencode_root.sh
├── pacstall/                     # Mantenimiento del gestor Pacstall
│   └── reparar_pacstall.sh
├── permisos/                     # Corrección de permisos de usuario ($HOME)
│   └── reparar_permisos.sh
├── pipewire_scrcpy/              # Audio PipeWire, WirePlumber y reglas udev ADB
│   └── reparar_pipewire_scrcpy.sh
├── retroarch/                    # Mantenimiento y logs de RetroArch (Flatpak)
│   └── reparar_retroarch.sh
├── sistema_y_mantenimiento/      # Limpieza general, GRUB, systemd, /var/crash
│   ├── corregir_errores_sistema.sh
│   ├── corregir_sistema_root.sh
│   ├── fix_errors.sh
│   ├── fix_system_errors.sh
│   ├── fix_system_issues.sh
│   ├── reparar_errores_sistema.sh
│   ├── reparar_sistema_y_logs.sh
│   ├── resolver_errores.sh
│   └── solucionar_errores.sh
├── variety_fondo_pantalla/       # Adaptación de fondos Variety para XFCE 4.20
│   └── set_wallpaper_parcheado.sh
├── waydroid_y_wayland/           # Contenedor Waydroid, Cage (X11) y Portales OBS
│   ├── iniciar_waydroid.sh
│   └── reparar_wayland_waydroid_obs.sh
├── README.md                     # Este archivo de referencia
└── GUIA_DIDACTICA.md             # Guía formativa teórica y práctica detallada
```

### Tabla Resumen de Scripts

| Categoría | Script | Privilegio | Descripción Breve |
| :--- | :--- | :---: | :--- |
| **dpkg_apt** | `reparar_dpkg.sh` | Root (`sudo`) | Elimina bloqueos, repara dependencias y purga paquetes en estado residual (`rc`). |
| **engrampa** | `reparar_engrampa_root.sh` | Root (`sudo`) | Soluciona fallos de segmentación y soporte RAR 7.x recompilando Engrampa. |
| **memoria_swap** | `setup_swap.sh` | Root (`sudo`) | Calcula tamaño ideal según RAM, crea `/swapfile` y optimiza `swappiness`. |
| **opencode** | `instalar_opencode_root.sh` | Root (`sudo`) | Instala y enlaza globalmente el CLI de OpenCode AI con permisos adecuados. |
| **pacstall** | `reparar_pacstall.sh` | Root (`sudo`) | Mantenimiento, actualización de repositorios y saneamiento de Pacstall. |
| **permisos** | `reparar_permisos.sh` | Root (`sudo`) | Restaura propiedad y permisos en `.config`, `.cache` y `.local` del usuario. |
| **pipewire_scrcpy** | `reparar_pipewire_scrcpy.sh` | Root (`sudo`) | Instala `libspa-0.2-libcamera`, reglas udev Android y reinicia WirePlumber. |
| **retroarch** | `reparar_retroarch.sh` | Usuario | Configura rutas, repara configs y directorios de log para RetroArch Flatpak. |
| **sistema_y_mantenimiento** | `corregir_errores_sistema.sh` | Root (`sudo`) | Limpia `apport`/`/var/crash`, corrige PAM de XFCE, Postfix, Snap, Flatpak, DPKG y GRUB. |
| **sistema_y_mantenimiento** | `corregir_sistema_root.sh` | Root (`sudo`) | Mantenimiento integral: VMware, reglas udev, Flatpak, syslog y GRUB. |
| **sistema_y_mantenimiento** | `fix_errors.sh` | Root (`sudo`) | Regenera `/boot/grub/grubenv` para solventar errores de arranque. |
| **sistema_y_mantenimiento** | `fix_system_errors.sh` | Root (`sudo`) | Limpieza de volcados huérfanos en `/var/crash` y saneamiento de logs. |
| **sistema_y_mantenimiento** | `fix_system_issues.sh` | Root (`sudo`) | Detección de anomalías en logs y depuración de reportes del sistema. |
| **sistema_y_mantenimiento** | `reparar_errores_sistema.sh` | Root (`sudo`) | Soluciona GID `uinput`, usuarios D-Bus malcontent, systemd y paquetes. |
| **sistema_y_mantenimiento** | `reparar_sistema_y_logs.sh` | Root (`sudo`) | Corrección de fallos en Firefox, Thunderbird, Flatpak, Snap, Xsession y GRUB. |
| **sistema_y_mantenimiento** | `resolver_errores.sh` | Root (`sudo`) | Módulo DKMS Droidcam, enmascara Bluetooth ausente y deshabilita `kvm_amd`. |
| **sistema_y_mantenimiento** | `solucionar_errores.sh` | Root (`sudo`) | Resetea `recordfail` en GRUB y subsana errores críticos del sistema. |
| **variety_fondo_pantalla** | `set_wallpaper_parcheado.sh` | Usuario | Adapta el cambiador Variety al subsistema Xfconf de XFCE 4.20. |
| **waydroid_y_wayland** | `iniciar_waydroid.sh` | Usuario | Lanza Waydroid en Wayland nativo o encapsulado en Cage si se está en X11. |
| **waydroid_y_wayland** | `reparar_wayland_waydroid_obs.sh` | Root (`sudo`) | Instala portales WLR, compositor Cage y configura captura en OBS Studio. |

---

## 🇬🇧 Overview (English)

This repository holds a structured suite of Bash scripts built to troubleshoot, repair, optimize, and maintain Linux operating system components (Ubuntu/Debian) as well as desktop user applications.

Each script is placed in a dedicated folder categorizing the targeted system domain or application.

### Quick Usage Guidelines

1. **Verify executable permissions:**
   ```bash
   chmod +x /home/bender/Descargas/scripts_reparacion/*/*.sh
   ```

2. **Executing Root Scripts:**
   Scripts that modify kernel parameters, drivers, package managers, or `/var` directories require administrative privileges:
   ```bash
   sudo bash /home/bender/Descargas/scripts_reparacion/<categoria>/<script>.sh
   ```

3. **Executing User-Space Scripts:**
   Scripts managing user configurations, Flatpak user sandboxes, or graphical sessions should **NOT** be launched with `sudo`:
   ```bash
   bash /home/bender/Descargas/scripts_reparacion/waydroid_y_wayland/iniciar_waydroid.sh
   bash /home/bender/Descargas/scripts_reparacion/retroarch/reparar_retroarch.sh
   ```

4. **Educational Guide:**
   For an in-depth breakdown of how Linux processes, memory management, systemd units, and D-Bus interfaces operate behind each script, read [GUIA_DIDACTICA.md](GUIA_DIDACTICA.md).
