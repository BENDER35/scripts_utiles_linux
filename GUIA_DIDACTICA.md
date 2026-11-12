# Guía Didáctica: Administración, Mantenimiento y Reparación de Linux
# Didactic Guide: Linux Administration, Maintenance & Troubleshooting

Esta guía didáctica explica paso a paso los fundamentos teóricos, los diagnósticos prácticos y las soluciones técnicas implementadas en los scripts organizados en `scripts_reparacion/`.

This educational manual breaks down the theoretical foundations, diagnostic workflows, and technical solutions implemented within the `scripts_reparacion/` repository.

---

## Índice / Table of Contents
1. [Módulo 1: Gestión de Paquetes (DPKG, APT y Pacstall) / Package Management](#módulo-1-gestión-de-paquetes-dpkg-apt-y-pacstall--package-management)
2. [Módulo 2: Subsistema de Arranque, Núcleo y Servicios / Boot Subsystem, Kernel & Services](#módulo-2-subsistema-de-arranque-núcleo-y-servicios--boot-subsystem-kernel--services)
3. [Módulo 3: Memoria Virtual y Swap / Virtual Memory & Swap](#módulo-3-memoria-virtual-y-swap--virtual-memory--swap)
4. [Módulo 4: Permisos y Espacio de Usuario / Permissions & User Space](#módulo-4-permisos-y-espacio-de-usuario--permissions--user-space)
5. [Módulo 5: Servidores Gráficos, Wayland y Contenedores / Display Servers, Wayland & Containers](#módulo-5-servidores-gráficos-wayland-y-contenedores--display-servers-wayland--containers)
6. [Módulo 6: Audio (PipeWire) y Dispositivos (UDEV / Scrcpy) / Audio & Device Access](#módulo-6-audio-pipewire-y-dispositivos-udev--scrcpy--audio--device-access)
7. [Módulo 7: Aplicaciones Específicas y Sandboxes / Dedicated Apps & Sandboxes](#módulo-7-aplicaciones-específicas-y-sandboxes--dedicated-apps--sandboxes)
8. [Glosario de Comandos Esenciales / Essential Commands Glossary](#glosario-de-comandos-esenciales--essential-commands-glossary)

---

## Módulo 1: Gestión de Paquetes (DPKG, APT y Pacstall) / Package Management

### 🇪🇸 Fundamento Teórico (Español)
En distribuciones basadas en Debian/Ubuntu:
- **DPKG (`dpkg`)** es la herramienta de bajo nivel encargada de desempaquetar, configurar y desinstalar paquetes binarios `.deb`.
- **APT (`apt`, `apt-get`)** es la capa superior que gestiona repositorios, resolución de dependencias complejas y descargas seguras vía HTTPS.
- **Pacstall** es un gestor de paquetes de terceros (estilo AUR de Arch Linux) diseñado para compilar paquetes desde código fuente o instalar versiones bleeding-edge en Ubuntu.

#### Problemas Comunes:
1. **Ficheros de Bloqueo Huérfanos (`lock` / `lock-frontend`):** Si un proceso de actualización (como `unattended-upgrades` o una terminal interrumpida con Ctrl+C) se cancela abruptamente, los archivos de bloqueo quedan en `/var/lib/dpkg/lock-frontend` y `/var/lib/apt/lists/lock`, impidiendo cualquier otra operación.
2. **Paquetes a medio configurar (`half-configured`) o rotos:** DPKG interrumpe la instalación si falla un script posterior a la instalación (`postinst`).
3. **Paquetes residuales (`rc`):** Paquetes cuyos binarios se eliminaron pero conservan archivos de configuración dispersos.

### 🇬🇧 Theory & Mechanics (English)
In Debian/Ubuntu architectures:
- **DPKG** operates at low level, unpacking `.deb` archives and running pre/post-installation maintainer scripts.
- **APT** coordinates dependency trees, network fetching, and repository mirrors.
- **Pacstall** serves as an AUR-like engine for Ubuntu, fetching recipes (`pacscript`) and compiling sources directly.

#### Scripts de este módulo:
* [`dpkg_apt/reparar_dpkg.sh`](dpkg_apt/reparar_dpkg.sh)
* [`pacstall/reparar_pacstall.sh`](pacstall/reparar_pacstall.sh)

#### Procedimiento de Reparación Aplicado:
```bash
# 1. Configurar paquetes desatendidos
sudo dpkg --configure -a

# 2. Forzar resolución y descarga de dependencias rotas
sudo apt-get install -f -y

# 3. Purgar configuraciones residuales (estado 'rc')
dpkg -l | awk '/^rc/ {print $2}' | xargs -r sudo dpkg --purge

# 4. Saneamiento de caché
sudo apt-get clean && sudo apt-get autoremove -y
```

---

## Módulo 2: Subsistema de Arranque, Núcleo y Servicios / Boot Subsystem, Kernel & Services

### 🇪🇸 Fundamento Teórico (Español)
El ciclo de arranque de Linux comienza con el firmware (UEFI/BIOS), que entrega el control a **GRUB2**. GRUB carga el **Kernel Linux** y la imagen de disco en memoria (**initramfs**), que a su vez ejecuta **systemd** (PID 1).

#### Problemas Comunes y Diagnósticos:
1. **Corrupción de `/boot/grub/grubenv`:** 
   El archivo `grubenv` es un bloque sin formato de exactamente 1024 bytes utilizado por GRUB para guardar variables de estado (por ejemplo, si el último arranque falló con `recordfail=1`). Si se corrompe por un apagón o escritura errónea, `systemctl` fallará con el servicio `grub-initrd-fallback.service`.
2. **Módulos de Kernel Incompatibles (`kvm_amd` en Intel):**
   Si una máquina tiene CPU Intel, el intento recurrente del sistema de cargar `kvm_amd` genera advertencias constantes en `journalctl`.
3. **Servicios de hardware inexistente:**
   Demonios como `bluetooth.service` consumen recursos e intentan activarse repetidamente mediante D-Bus si el equipo no posee tarjeta física Bluetooth.
4. **Volcados de error en `/var/crash`:**
   El demonio `apport` genera archivos `.crash` voluminosos cuando un programa falla. Si no se limpian periódicamente, llenan la partición raíz (`/`).
5. **Pila PAM incompleta en `xfce4-screensaver`:**
   Si `/etc/pam.d/xfce4-screensaver` carece de la regla `common-account`, el diálogo de desbloqueo falla y genera errores PAM en el Journal. Además, `apport-autoreport.service` puede quedar en estado `failed` tras acumular volcados en `/var/crash`.

### 🇬🇧 Theory & Mechanics (English)
The boot sequence hands off from firmware to **GRUB2**, which stages kernel parameters and initiates **systemd**.

- **GRUB Environment Block (`grubenv`):** A rigid 1024-byte block storing boot counter flags. Corrupted sectors cause `grub-editenv` read errors and systemd service failures.
- **Kernel Modules & Modprobe:** Blacklisting unsupported virtualization drivers (e.g., preventing AMD KVM on Intel silicon) eliminates noise in kernel logs (`dmesg`).
- **PAM stacks for screen lockers:** Missing `common-account` includes in `/etc/pam.d/xfce4-screensaver` break unlock authentication. Resetting `apport-autoreport` and purging crash dumps clears stale failure states.

#### Scripts de este módulo:
* [`sistema_y_mantenimiento/corregir_errores_sistema.sh`](sistema_y_mantenimiento/corregir_errores_sistema.sh)
* [`sistema_y_mantenimiento/fix_errors.sh`](sistema_y_mantenimiento/fix_errors.sh)
* [`sistema_y_mantenimiento/solucionar_errores.sh`](sistema_y_mantenimiento/solucionar_errores.sh)
* [`sistema_y_mantenimiento/resolver_errores.sh`](sistema_y_mantenimiento/resolver_errores.sh)
* [`sistema_y_mantenimiento/reparar_errores_sistema.sh`](sistema_y_mantenimiento/reparar_errores_sistema.sh)
* [`sistema_y_mantenimiento/corregir_sistema_root.sh`](sistema_y_mantenimiento/corregir_sistema_root.sh)
* [`sistema_y_mantenimiento/reparar_sistema_y_logs.sh`](sistema_y_mantenimiento/reparar_sistema_y_logs.sh)
* [`sistema_y_mantenimiento/fix_system_errors.sh`](sistema_y_mantenimiento/fix_system_errors.sh)
* [`sistema_y_mantenimiento/fix_system_issues.sh`](sistema_y_mantenimiento/fix_system_issues.sh)

#### Procedimiento de Reparación Aplicado:
```bash
# Recrear el bloque de entorno de GRUB limpio:
sudo rm -f /boot/grub/grubenv
sudo grub-editenv /boot/grub/grubenv create
sudo grub-editenv /boot/grub/grubenv set recordfail=0
sudo update-grub

# Enmascarar servicio sin soporte de hardware:
sudo systemctl mask bluetooth.service

# Bloquear carga de kvm_amd:
echo "install kvm_amd /bin/true" | sudo tee /etc/modprobe.d/disable-kvm-amd.conf

# Purgar informes de caídas huérfanos:
sudo rm -rf /var/crash/*

# Reparar la pila PAM del salvapantallas de XFCE:
sudo grep -q common-account /etc/pam.d/xfce4-screensaver || \
  printf '@include common-auth\n@include common-account\n@include common-password\n@include common-session\n' | sudo tee /etc/pam.d/xfce4-screensaver

# Resetear el estado de apport y sanear el chroot de Postfix:
sudo systemctl reset-failed apport-autoreport.service
sudo chown root:root /var/spool/postfix/etc/resolv.conf
sudo chmod 644 /var/spool/postfix/etc/resolv.conf
```

---

## Módulo 3: Memoria Virtual y Swap / Virtual Memory & Swap

### 🇪🇸 Fundamento Teórico (Español)
La **Memoria Swap** es un espacio en disco (partición o fichero) que el kernel Linux utiliza como extensión de la memoria RAM mediante paginación. Cuando la memoria física escasea, las páginas inactivas se transfieren a la Swap para evitar que el mecanismo **OOM Killer** (Out-Of-Memory Killer) termine procesos críticos.

#### Parámetros Clave del Kernel:
- **`vm.swappiness` (0 a 100):** Determina la agresividad con la que el kernel intercambia memoria anónima por swap frente a desalojar páginas de caché del sistema de archivos (`page cache`). Un valor de 10 a 60 es recomendado para escritorios y estaciones de trabajo modernas.
- **Seguridad (`chmod 600`):** Dado que la Swap contiene volcados crudos de la RAM (que pueden incluir contraseñas y claves privadas), **solo root** debe tener permisos de lectura y escritura.

### 🇬🇧 Theory & Mechanics (English)
Virtual memory pages out inactive segments to non-volatile storage to protect system responsiveness and prevent system crashes caused by OOM events.

#### Script de este módulo:
* [`memoria_swap/setup_swap.sh`](memoria_swap/setup_swap.sh)

#### Procedimiento Técnico de Creación:
```bash
# 1. Asignar espacio contiguo en disco (ej. 4GB o según RAM)
sudo fallocate -l 4G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 status=progress

# 2. Asegurar permisos restrictivos contra lecturas no autorizadas
sudo chmod 600 /swapfile

# 3. Formatear como estructura Swap e iniciarla
sudo mkswap /swapfile
sudo swapon /swapfile

# 4. Hacerlo persistente en fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Módulo 4: Permisos y Espacio de Usuario / Permissions & User Space

### 🇪🇸 Fundamento Teórico (Español)
En el modelo de seguridad POSIX de Linux:
- Cada archivo y carpeta pertenece a un `Usuario` (UID) y a un `Grupo` (GID).
- Un error muy común ocurre cuando el usuario ejecuta comandos gráficos o herramientas de desarrollo precedidas de `sudo` (ej: `sudo pip install`, `sudo app`). Esto crea carpetas dentro de `/home/$USER/` con propietario `root:root`.
- Como consecuencia, el usuario normal pierde acceso a su propia base de datos de configuraciones (`~/.cache/dconf`), perdiendo ajustes visuales, asociaciones de archivos en `mimeapps.list` o provocando cierres inesperados en aplicaciones de escritorio.

### 🇬🇧 Theory & Mechanics (English)
Running utilities inside `$HOME` using `sudo` pollutes the home directory hierarchy with `root:root` ownership, breaking desktop session IPC, dconf databases, and MIME type caches.

#### Script de este módulo:
* [`permisos/reparar_permisos.sh`](permisos/reparar_permisos.sh)

#### Procedimiento Técnico de Corrección:
```bash
# Restaurar la propiedad legítima al usuario:
sudo chown -R bender:bender /home/bender/.config /home/bender/.cache /home/bender/.local

# Asegurar permisos estrictos en la base de datos de dconf (evita lectura por terceros):
chmod 700 /home/bender/.cache/dconf
```

---

## Módulo 5: Servidores Gráficos, Wayland y Contenedores / Display Servers, Wayland & Containers

### 🇪🇸 Fundamento Teórico (Español)
Linux está en transición de **X11** (X.Org) a **Wayland**:
- **Wayland** es un protocolo moderno donde cada ventana está aislada y el compositor se encarga directamente del renderizado sin servidor intermedio.
- **Waydroid** es un entorno de contenedorización basado en LXC que ejecuta un sistema Android completo sobre el kernel Linux del anfitrión mediante `binder` y `ashmem`. Waydroid requiere de forma estricta un compositor Wayland para renderizar su interfaz.
- **Problema de compatibilidad:** Si el usuario tiene una sesión gráfica X11 (como XFCE tradicional), Waydroid falla. Para solucionarlo, se puede usar **`cage`**, un compositor Wayland kiosco que se ejecuta anidado dentro de una ventana de X11.
- **Portales XDG y OBS:** En Wayland, una aplicación no puede espiar la pantalla de otra. Para capturar video en OBS Studio, se requiere `xdg-desktop-portal-wlr` junto con PipeWire para compartir el flujo de video con consentimiento explícito del compositor.

### 🇬🇧 Theory & Mechanics (English)
Wayland isolates graphical surfaces. Applications like Waydroid depend natively on Wayland buffers. When running under an X11 desktop, a nested compositor such as `cage` provides an in-window Wayland canvas. Capturing video (via OBS Studio) relies on standard `xdg-desktop-portal` IPC bridges over PipeWire.

#### Scripts de este módulo:
* [`waydroid_y_wayland/iniciar_waydroid.sh`](waydroid_y_wayland/iniciar_waydroid.sh)
* [`waydroid_y_wayland/reparar_wayland_waydroid_obs.sh`](waydroid_y_wayland/reparar_wayland_waydroid_obs.sh)
* [`variety_fondo_pantalla/set_wallpaper_parcheado.sh`](variety_fondo_pantalla/set_wallpaper_parcheado.sh)

---

## Módulo 6: Audio (PipeWire) y Dispositivos (UDEV / Scrcpy) / Audio & Device Access

### 🇪🇸 Fundamento Teórico (Español)
- **PipeWire y WirePlumber:** PipeWire unifica el procesamiento de audio y vídeo de baja latencia en Linux. **WirePlumber** es su gestor de políticas y sesiones. La falta de módulos SPA (como `libspa-0.2-libcamera`) genera fallos y mensajes de advertencia continuos al negociar nodos multimedia.
- **Reglas UDEV:** El subsistema de UDEV asigna dinámicamente nodos en `/dev/` cuando se conecta hardware por USB. Para que aplicaciones como **Scrcpy** o **ADB** puedan comunicarse con teléfonos Android sin necesidad de usar `sudo`, el paquete `android-udev-rules` añade reglas que otorgan permisos al grupo local `plugdev` o `adbusers`.

### 🇬🇧 Theory & Mechanics (English)
- **PipeWire Architecture:** Dynamic low-latency media graph coordinated by WirePlumber. Missing SPA (Simple Plugin API) packages trigger negotiation stalls.
- **UDEV Rules:** Dynamic device node permission granting for USB peripherals. Installing `android-udev-rules` avoids root requirement when communicating via ADB/Scrcpy.

#### Script de este módulo:
* [`pipewire_scrcpy/reparar_pipewire_scrcpy.sh`](pipewire_scrcpy/reparar_pipewire_scrcpy.sh)

#### Procedimiento Técnico:
```bash
# Instalar plugins SPA requeridos:
sudo apt-get install -y libspa-0.2-libcamera android-udev-rules

# Recargar reglas udev en caliente:
sudo udevadm control --reload-rules && sudo udevadm trigger

# Reiniciar sesión de WirePlumber en el espacio de usuario:
systemctl --user restart wireplumber.service
```

---

## Módulo 7: Aplicaciones Específicas y Sandboxes / Dedicated Apps & Sandboxes

### 🇪🇸 Fundamento Teórico (Español)
1. **Engrampa (`reparar_engrampa_root.sh`):**
   Engrampa es el archivador de escritorio de MATE/XFCE. La versión estándar sufría fallos críticos de segmentación (`SIGSEGV`) y vulnerabilidades de seguridad (CVE-2023-52138) al procesar archivos RAR generados con la versión 7.x. Este script parchea el código fuente y recompila el paquete en Debian/Ubuntu para habilitar soporte total de contraseñas y estabilidad.
2. **RetroArch en Flatpak (`reparar_retroarch.sh`):**
   Las aplicaciones Flatpak se ejecutan en un contenedor aislado con su propio `$HOME` virtual en `~/.var/app/org.libretro.RetroArch/`. Si los directorios de shaders, logs o configuración no coinciden con los permisos del contenedor, RetroArch puede perder perfiles de mandos o fallar silenciosamente al iniciar cores.
3. **OpenCode AI (`instalar_opencode_root.sh`):**
   Integra de forma global binarios basados en entornos Node/NVM creando enlaces simbólicos protegidos en `/usr/local/bin` con resolución de rutas del usuario original mediante `$SUDO_USER`.
4. **Steam (`reparar_steam_root.sh`):**
   El cliente de Steam invoca `steamdeps` mediante la cabecera `#!/usr/bin/env python3`. Si Homebrew/Linuxbrew está instalado, esa ruta resuelve primero al Python de Homebrew (por ejemplo, 3.15) en lugar del Python del sistema (3.14), lo que provoca el error `Couldn't import apt`. El script reescribe la cabecera de `/usr/lib/steam/bin_steamdeps.py` para usar `/usr/bin/python3`, reinstala `python3-apt` y las librerías de Steam, y valida el resultado con `steamdeps --dry-run`.

### 🇬🇧 Theory & Mechanics (English)
1. **Engrampa Patching:** Resolves memory corruption and CVE-2023-52138 path-traversal vulnerabilities with upstream patches compiled locally.
2. **Flatpak Sandboxing:** Isolates runtime configs under `~/.var/app/` requiring synchronized user namespaces.
3. **OpenCode AI Global Binding:** Hooks user-level node installations into `/usr/local/bin` preserving legitimate environment paths.
4. **Steam Dependency Resolution:** Steam's `steamdeps` helper uses `#!/usr/bin/env python3`, which can resolve to a Homebrew interpreter without Debian's `apt` bindings. Pinning the shebang to the system Python restores the `python3-apt` module used by Steam's package checks.

#### Scripts de este módulo:
* [`engrampa/reparar_engrampa_root.sh`](engrampa/reparar_engrampa_root.sh)
* [`retroarch/reparar_retroarch.sh`](retroarch/reparar_retroarch.sh)
* [`opencode/instalar_opencode_root.sh`](opencode/instalar_opencode_root.sh)
* [`steam/reparar_steam_root.sh`](steam/reparar_steam_root.sh)

#### Procedimiento Técnico:
```bash
# Forzar el intérprete Python del sistema en steamdeps:
sudo sed -i 's|^#!/usr/bin/env python3|#!/usr/bin/python3|' /usr/lib/steam/bin_steamdeps.py

# Reinstalar el enlace de python3-apt y las librerías de Steam:
sudo apt-get update
sudo apt-get install -y --no-remove python3-apt steam-libs-amd64 steam-libs-i386

# Validar que steamdeps ya importa apt correctamente:
sudo /usr/bin/steamdeps --dry-run
```

---

## Glosario de Comandos Esenciales / Essential Commands Glossary

| Comando / Command | Función Principal / Main Purpose | Nivel de Riesgo / Risk |
| :--- | :--- | :---: |
| `systemctl status <unidad>` | Inspecciona el estado de un servicio del sistema. | Inocuo (Lectura) |
| `journalctl -xeu <unidad>` | Muestra logs detallados de error de un servicio específico. | Inocuo (Lectura) |
| `dpkg --configure -a` | Configura paquetes pendientes desempaquetados. | Seguro / Reparación |
| `apt-get install -f` | Repara el árbol de dependencias rotas del sistema. | Seguro / Reparación |
| `udevadm control --reload` | Recarga reglas de hardware USB/dispositivos sin reiniciar. | Seguro |
| `grub-editenv create` | Crea un bloque de entorno vacío para GRUB2. | Moderado (Requiere root) |
| `fallocate -l <tamaño> <ruta>` | Reserva espacio continuo en disco para archivos Swap. | Moderado (Espacio) |
| `chown -R <user>:<group> <ruta>` | Reasigna la propiedad de archivos y subdirectorios. | Moderado |
| `sed -i 's/.../.../' <archivo>` | Sustituye texto en un archivo in situ (usado para corregir el shebang de `steamdeps`). | Moderado (Requiere backup) |
| `/usr/bin/steamdeps --dry-run` | Valida las dependencias de Steam sin instalar paquetes. | Inocuo (Lectura) |
