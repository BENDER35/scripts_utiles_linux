# -*- coding: utf-8 -*-
import subprocess
import os

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Manual Técnico: Root, Bootloader y Custom ROMs en TCL 40 SE y Tablets TCL</title>
<style>
  body {
    font-family: 'Liberation Sans', Arial, Helvetica, sans-serif;
    color: #24292e;
    line-height: 1.6;
    margin: 40px;
  }
  h1 {
    color: #0b5394;
    border-bottom: 3px solid #0b5394;
    padding-bottom: 8px;
    font-size: 26pt;
    margin-top: 0;
  }
  h2 {
    color: #1155cc;
    border-bottom: 1.5px solid #cccccc;
    padding-bottom: 5px;
    font-size: 18pt;
    margin-top: 25px;
  }
  h3 {
    color: #134f5c;
    font-size: 14pt;
    margin-top: 18px;
  }
  p, li {
    font-size: 11pt;
  }
  .alert-warning {
    background-color: #fff2cc;
    border-left: 6px solid #f1c232;
    padding: 14px 18px;
    margin: 18px 0;
    border-radius: 4px;
  }
  .alert-danger {
    background-color: #fce5cd;
    border-left: 6px solid #e69138;
    padding: 14px 18px;
    margin: 18px 0;
    border-radius: 4px;
  }
  .alert-info {
    background-color: #d9ead3;
    border-left: 6px solid #6aa84f;
    padding: 14px 18px;
    margin: 18px 0;
    border-radius: 4px;
  }
  pre {
    background-color: #f3f3f3;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    padding: 12px;
    font-family: 'Liberation Mono', Consolas, 'Courier New', monospace;
    font-size: 10pt;
    overflow-x: auto;
  }
  code {
    background-color: #efefef;
    padding: 2px 5px;
    border-radius: 3px;
    font-family: 'Liberation Mono', Consolas, 'Courier New', monospace;
    font-size: 10pt;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    font-size: 10.5pt;
  }
  th, td {
    border: 1px solid #b7b7b7;
    padding: 10px 12px;
    text-align: left;
  }
  th {
    background-color: #cfe2f3;
    color: #0b5394;
    font-weight: bold;
  }
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  a {
    color: #1155cc;
    text-decoration: underline;
  }
  ul, ol {
    margin-left: 20px;
  }
  .footer {
    margin-top: 40px;
    border-top: 1px solid #ddd;
    padding-top: 10px;
    font-size: 9pt;
    color: #666;
  }
</style>
</head>
<body>

<h1>Manual Técnico: Root, Bootloader y Custom ROMs en TCL 40 SE y Tablets TCL</h1>
<p><strong>Fecha de elaboración:</strong> Octubre 2026 | <strong>Autor:</strong> Antigravity AI | <strong>Formato:</strong> OpenDocument Text (.odt)</p>

<div class="alert-info">
  <strong>Resumen Ejecutivo:</strong>
  Este informe y manual técnico detalla la viabilidad, limitaciones de seguridad del fabricante, catálogo de ROMs disponibles y el protocolo técnico paso a paso para rootear e instalar sistemas operativos personalizados en el teléfono <strong>TCL 40 SE</strong> (variantes T610K, T610E, T610P) y en tablets de la marca TCL (con especial cobertura para la gama <strong>TCL NXTPAPER 11 / NXTPAPER Series</strong>).
</div>

---

<h2>1. Diagnóstico de Viabilidad: ¿Es Posible Hacer Root al TCL 40 SE y a las Tablets TCL?</h2>

<h3>1.1. Arquitectura de Hardware</h3>
<ul>
  <li><strong>TCL 40 SE:</strong> Equipado con SoC <strong>MediaTek Helio G37 (MT6765V/CB)</strong> de 12 nm, arquitectura ARM64 (arm64-v8a), con sistema operativo de fábrica Android 13 bajo la capa TCL UI 5.0.</li>
  <li><strong>Tablets TCL (NXTPAPER 11 / NXTPAPER 11 Plus):</strong> Basadas predominantemente en el SoC <strong>MediaTek Helio P60T (MT8788)</strong>, también de arquitectura ARM64, con Android 13 y panel con optimizaciones ópticas NxtVision.</li>
</ul>

<h3>1.2. La Barrera del Bootloader (Cargador de Arranque)</h3>
<p>
Para obtener acceso de administrador (<strong>Root</strong>) mediante el método estándar moderno (parcheo de <code>boot.img</code> con <strong>Magisk</strong>) o para instalar cualquier sistema modificado, es imprescindible que el <strong>Bootloader esté desbloqueado</strong>.
</p>
<ul>
  <li><strong>Comportamiento del fabricante TCL:</strong> Aunque en las <em>Opciones de desarrollador</em> de Android exista el interruptor "Desbloqueo de OEM", TCL <strong>bloquea o anula deliberadamente</strong> los comandos estándar de Fastboot en sus terminales comerciales:
    <pre>fastboot flashing unlock
# Salida típica de error:
# FAILED (remote: 'Flashing Unlock is not allowed') o FAILED (remote: 'unknown command')</pre>
  </li>
  <li><strong>Consecuencia:</strong> A diferencia de dispositivos Google Pixel, Xiaomi, Motorola o OnePlus, no existe un método oficial o trivial provisto por TCL para desbloquear el bootloader desde la línea de comandos estándar.</li>
</ul>

<h3>1.3. La Vía Técnica Real: Explotación BROM con MediaTek Client (mtkclient)</h3>
<p>
Dado que ambos dispositivos emplean procesadores MediaTek, la única vía factible para saltarse las protecciones de TCL a nivel de software sin recurrir a hardware comercial cerrado consiste en interactuar directamente con la <strong>BootROM (BROM)</strong> de MediaTek utilizando la herramienta de código abierto <strong>mtkclient</strong> (desarrollada por B. Kerler):
</p>
<ol>
  <li><strong>Bypass de SLA/DAA:</strong> La herramienta explota la vulnerabilidad de bajo nivel de la ROM de arranque para eludir la comprobación de autenticación de descarga (DA Auth / SLA) mediante un fallo forzado de handshake por USB.</li>
  <li><strong>Desbloqueo forzado de partición seccfg:</strong> Permite sobrescribir el registro de seguridad de arranque ejecutando:
    <pre>python3 mtk.py da seccfg unlock</pre>
  </li>
  <li><strong>Extracción directa de particiones:</strong> Permite volcar de forma limpia <code>boot.img</code> y <code>vbmeta.img</code> directamente de la memoria física eMMC/UFS para parcharlo con Magisk sin necesidad de localizar el firmware completo oficial en la red.</li>
</ol>

<div class="alert-warning">
  <strong>Limitación por Parches de Seguridad Modernos:</strong><br>
  En unidades con parches de seguridad recientes de Android 13/14, MediaTek y TCL han deshabilitado el punto de entrada directo USB para BROM en el preloader. Si el terminal no responde al conectar con botones de volumen pulsados (handshake BROM rechazado), se requerirá:
  <ul>
    <li>Abrir la carcasa trasera y hacer puente en el <strong>Testpoint físico (KCOLO a GND)</strong> para forzar BROM por hardware, o</li>
    <li>Utilizar herramientas comerciales de taller técnico (dongles de pago con autorizaciones propietarias como <em>Pandora Box</em>, <em>Chimera Tool</em> o <em>Furious Gold OTSMART</em>).</li>
  </ul>
</div>

<div class="alert-danger">
  <strong>ADVERTENCIA SOBRE APLICACIONES "ONE-CLICK ROOT":</strong><br>
  Herramientas del tipo KingRoot, KingoRoot, Framaroot, iRoot o OneClickRoot <strong>NO FUNCIONAN</strong> en Android 10, 11, 12 ni 13. Son aplicaciones obsoletas y potencialmente maliciosas que no pueden saltarse SELinux ni la verificación criptográfica AVB 2.0. <strong>No las instales bajo ninguna circunstancia.</strong>
</div>

---

<h2>2. Catálogo de Custom ROMs para TCL 40 SE y Tablets TCL</h2>

<h3>2.1. Estado de Desarrollo Dedicado</h3>
<p>
<strong>NO existen Custom ROMs oficiales ni compilaciones dedicadas</strong> (como LineageOS oficial, PixelOS oficial, Paranoid Android o crDroid oficial con árbol de dispositivo propio) específicamente desarrolladas para el TCL 40 SE ni para la tablet TCL NXTPAPER 11.
</p>
<p>
<strong>Motivo:</strong> TCL no publica de forma proactiva el código fuente completo del kernel ni los árboles de dispositivos (Device Trees / Vendor Blobs), lo que sumado a la cuota de mercado minoritaria entre entusiastas de XDA Developers provoca que ningún mantenedor mantenga builds nativos.
</p>

<h3>2.2. La Solución Real: Generic System Images (GSI) con Project Treble</h3>
<p>
Tanto el TCL 40 SE como las tablets TCL NXTPAPER llegaron al mercado con <strong>Android 13 de fábrica</strong>, lo que garantiza por especificación de Google el soporte pleno de <strong>Project Treble</strong> (partición <code>system</code> desacoplada de la partición <code>vendor</code> del fabricante).
</p>
<p>
Esto significa que <strong>sí es posible instalar Custom ROMs universales en formato GSI (Generic System Image)</strong> con arquitectura <strong>ARM64-ab (system-as-root)</strong>.
</p>

<h3>2.3. Las Mejores Custom ROMs GSI Compatibles</h3>

<table>
  <tr>
    <th>Nombre de la ROM GSI</th>
    <th>Desarrollador / Base</th>
    <th>Características Principales</th>
    <th>Variante Recomendada</th>
  </tr>
  <tr>
    <td><strong>LineageOS GSI</strong></td>
    <td>AndyCGYan (base TrebleDroid)</td>
    <td>Extremadamente ligera, excelente gestión de memoria RAM, máxima estabilidad en SoCs MediaTek modestos como Helio G37.</td>
    <td><code>arm64_bgN</code> (con GApps) o <code>arm64_bvN</code> (Vanilla)</td>
  </tr>
  <tr>
    <td><strong>PixelOS / Pixel Experience GSI</strong></td>
    <td>Ponces</td>
    <td>Interfaz limpia de Google Pixel, launcher Pixel oficial, integración nativa de servicios de Google, fondos animados y diseño Material You.</td>
    <td><code>arm64_bgN</code> (incluye GApps)</td>
  </tr>
  <tr>
    <td><strong>TrebleDroid AOSP GSI</strong></td>
    <td>Phhusson & TrebleDroid Team</td>
    <td>La base universal de código abierto de la que derivan la mayoría de GSIs. Implementa todos los parches y "quirks" para procesadores MediaTek.</td>
    <td><code>arm64_bvN</code> (AOSP puro)</td>
  </tr>
  <tr>
    <td><strong>crDroid GSI</strong></td>
    <td>Nazim / TrebleDroid</td>
    <td>Basada en LineageOS pero con decenas de ajustes adicionales de personalización visual, rendimiento y barra de estado.</td>
    <td><code>arm64_bgN</code> / <code>arm64_bvN</code></td>
  </tr>
  <tr>
    <td><strong>LeOS GSI</strong></td>
    <td>Harom / LeOS Team</td>
    <td>Orientada a la privacidad total, 100% desgooglizada (sin servicios ni telemetría de Google), ideal para usuarios que buscan autonomía extrema.</td>
    <td><code>arm64_bvN</code> (microG integrado)</td>
  </tr>
</table>

<p><em>Glosario de sufijos de compilación GSI:</em></p>
<ul>
  <li><code>arm64</code>: Arquitectura de 64 bits (compatible con Helio G37 / MT8788).</li>
  <li><code>b</code>: Formato de partición A/B (estándar en Android 10+).</li>
  <li><code>g</code>: Incluye Google Apps (GApps) preinstaladas.</li>
  <li><code>v</code>: Versión "Vanilla" sin servicios de Google (sistema limpio).</li>
  <li><code>N</code>: Sin superusuario integrado (recomendado para usar Magisk oficial).</li>
  <li><code>S</code>: Con superusuario integrado en el sistema.</li>
</ul>

<h3>2.4. Limitaciones y Advertencias de Hardware al Usar GSI en TCL</h3>
<div class="alert-warning">
  <strong>Comportamiento del Hardware bajo una ROM GSI:</strong>
  <ul>
    <li><strong>Pérdida de NxtVision y Modo Papel:</strong> En las tablets TCL NXTPAPER 11, la tecnología de pantalla antirreflejos y los modos de color (papel de tinta electrónica, lectura, etc.) son controlados por software privativo de TCL. En una GSI genérica, la pantalla funcionará como un panel estándar y se perderá el control de estos modos especializados.</li>
    <li><strong>Cámaras Auxiliares:</strong> Solo la lente principal de 50 MP (en TCL 40 SE) funcionará de forma básica mediante la API Camera2. Las lentes secundarias (macro y profundidad) suelen quedar inactivas.</li>
    <li><strong>Llamadas VoLTE / IMS:</strong> MediaTek utiliza implementaciones de red propietarias que en ocasiones provocan distorsiones o fallos en el audio de llamadas en GSIs a menos que se habiliten los parches de Treble en los ajustes específicos de Phh.</li>
    <li><strong>DRM Widevine L1:</strong> Al desbloquear el bootloader, la certificación Widevine descenderá a <strong>L3</strong>, limitando la reproducción en Netflix, Disney+ o Prime Video a resolución SD (480p/540p).</li>
  </ul>
</div>

---

<h2>3. Manual Paso a Paso: Desbloqueo de Bootloader, Magisk Root e Instalación de ROM</h2>

<div class="alert-danger">
  <strong>ADVERTENCIA DE RESPONSABILIDAD:</strong><br>
  El desbloqueo del bootloader y la manipulación de particiones críticas borra absolutamente todos los datos del terminal y puede dejar el dispositivo inservible (hard brick) si se comete un error. Realiza una copia de seguridad externa completa antes de proceder.
</div>

<h3>Fase 1: Preparación del Entorno en la Computadora (Linux)</h3>
<p>Recomendamos realizar todo el proceso en Linux (como tu sistema actual Ubuntu/Debian), ya que el manejo de puertos USB y permisos de bajo nivel de MediaTek es infinitamente más estable que en Windows.</p>

<p>1. Instalar herramientas ADB, Fastboot, Python3 y dependencias de compilación USB:</p>
<pre>sudo apt update
sudo apt install -y android-tools-adb android-tools-fastboot python3 python3-pip git libusb-1.0-0-dev libudev-dev</pre>

<p>2. Descargar y preparar <strong>mtkclient</strong>:</p>
<pre>cd ~/Descargas
git clone https://github.com/bkerler/mtkclient.git
cd mtkclient
pip3 install -r requirements.txt</pre>

<p>3. Configurar reglas de UDEV para que el sistema reconozca el dispositivo MediaTek en modo BROM sin requerir permisos de superusuario manuales:</p>
<pre>sudo usermod -aG plugdev $USER
sudo usermod -aG dialout $USER
sudo cp Setup/udev/51-edl.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger</pre>

<p>4. Detener el servicio <code>modemmanager</code> para evitar que interfiera con los puertos serie temporales de MediaTek:</p>
<pre>sudo systemctl stop ModemManager
sudo systemctl disable ModemManager</pre>

---

<h3>Fase 2: Respaldo Completo de Seguridad y Desbloqueo de Bootloader</h3>

<p>1. <strong>Activar opciones de desarrollo en el teléfono / tablet:</strong></p>
<ul>
  <li>Ir a <em>Ajustes</em> &gt; <em>Información del teléfono / tablet</em>.</li>
  <li>Pulsar 7 veces sobre <em>Número de compilación</em> hasta activar las Opciones de desarrollador.</li>
  <li>Ir a <em>Ajustes</em> &gt; <em>Sistema</em> &gt; <em>Opciones de desarrollador</em>.</li>
  <li>Habilitar <strong>Depuración USB</strong> y <strong>Desbloqueo de OEM</strong>.</li>
</ul>

<p>2. <strong>Hacer un volcado de respaldo vital (NVRAM, NVDATA, Boot, VBMeta):</strong></p>
<p>Apaga el teléfono por completo. En la terminal de la PC, dentro de la carpeta <code>mtkclient</code>, ejecuta:</p>
<pre># Preparar lectura de particiones críticas
python3 mtk.py r nvram,nvdata,protect1,protect2,boot,vbmeta nvram.img,nvdata.img,protect1.img,protect2.img,boot.img,vbmeta.img</pre>
<p>
<em>Acción con el dispositivo:</em> Con el teléfono <strong>completamente apagado</strong>, mantén presionados los botones <strong>Volumen Arriba (+) y Volumen Abajo (-)</strong> simultáneamente y conecta el cable USB a la PC. En cuanto mtkclient detecte el dispositivo (aparecerá "Device detected" y el handshake BROM), suelta los botones. Se volcarán las particiones a tu disco duro.
</p>
<div class="alert-info">
  <strong>¡CONSERVA ESTOS ARCHIVOS!</strong> Los archivos <code>nvram.img</code> y <code>nvdata.img</code> contienen el número IMEI, calibración de radio y direcciones MAC de tu dispositivo. Si se corrompen sin respaldo, el teléfono perderá la cobertura telefónica para siempre.
</div>

<p>3. <strong>Desbloquear el Bootloader con mtkclient:</strong></p>
<p>Con el dispositivo desconectado y apagado, ejecuta:</p>
<pre>python3 mtk.py da seccfg unlock</pre>
<p>Vuelve a conectar el teléfono apagado manteniendo presionados ambos botones de volumen. Una vez complete el proceso con éxito, ejecuta:</p>
<pre>python3 mtk.py reset</pre>
<p>
El teléfono se reiniciará. Al encender, mostrará un aviso de <em>Orange State / Your device has been unlocked</em> y realizará un formateo de fábrica de los datos. Deja que inicie Android y configúralo de forma básica.
</p>

---

<h3>Fase 3: Obtención de Root con Magisk</h3>

<p>1. Descarga e instala en el teléfono la última versión oficial de la aplicación <strong>Magisk</strong> (desde el repositorio oficial de topjohnwu).</p>

<p>2. Transfiere el archivo <code>boot.img</code> (extraído en la Fase 2) a la memoria interna del teléfono:</p>
<pre>adb push boot.img /sdcard/Download/</pre>

<p>3. <strong>Parchear la imagen en el teléfono:</strong></p>
<ul>
  <li>Abre la aplicación <strong>Magisk</strong>.</li>
  <li>En la tarjeta superior (Magisk), pulsa en <strong>Instalar</strong>.</li>
  <li>Elige <strong>Seleccionar y parchar un archivo</strong>.</li>
  <li>Navega a la carpeta Descargas y selecciona <code>boot.img</code>.</li>
  <li>Pulsa en <strong>Comencemos</strong>. Magisk generará un archivo con un nombre similar a: <code>magisk_patched_XXXXX.img</code>.</li>
</ul>

<p>4. Extraer la imagen parcheada al PC:</p>
<pre>adb pull /sdcard/Download/magisk_patched_*.img ./magisk_patched_boot.img</pre>

<p>5. <strong>Flashear Boot parcheado y desactivar Android Verified Boot (AVB):</strong></p>
<p>Reinicia el dispositivo en modo Fastboot:</p>
<pre>adb reboot bootloader</pre>
<p>Verifica que fastboot responda:</p>
<pre>fastboot devices</pre>
<p>Flashea el boot parcheado y el archivo vbmeta con los flags obligatorios de deshabilitación de integridad:</p>
<pre>fastboot flash boot magisk_patched_boot.img
fastboot flash --disable-verity --disable-verification vbmeta vbmeta.img
fastboot reboot</pre>
<p>
Al reiniciar, abre la aplicación Magisk. Verás el estado <strong>"Instalado: v27.x / v28.x"</strong> con acceso Superusuario (Root) plenamente activo.
</p>

---

<h3>Fase 4: Instalación de una Custom ROM (GSI Treble)</h3>

<p>Si deseas reemplazar el software de TCL por una ROM limpia (como LineageOS o PixelOS):</p>

<p>1. <strong>Descargar la imagen GSI compatible:</strong></p>
<ul>
  <li>Descarga el archivo <code>.img.xz</code> (por ejemplo, <em>lineage-21.0-*-UNOFFICIAL-arm64_bgN.img.xz</em>).</li>
  <li>Descomprímelo en tu PC:
    <pre>unxz lineage-21.0-*-UNOFFICIAL-arm64_bgN.img.xz</pre>
    (Obtendrás un archivo <code>.img</code> de varios gigabytes).
  </li>
</ul>

<p>2. <strong>Entrar en Fastbootd (Modo Fastboot Dinámico):</strong></p>
<p>Los dispositivos con Android 10 o superior utilizan particiones lógicas (super partition). Las ROMs GSI deben flashearse en <strong>fastbootd</strong>, NO en el bootloader clásico:</p>
<pre>adb reboot fastboot
# O si ya estás en bootloader:
fastboot reboot fastboot</pre>
<p><em>En la pantalla del teléfono/tablet aparecerá un menú textual con la cabecera "Fastbootd".</em></p>

<p>3. <strong>Flashear la partición del sistema y formatear datos:</strong></p>
<pre># Desactivar verificación de firmas criptográficas
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# Borrar la partición system actual y flashear la nueva GSI
fastboot erase system
fastboot flash system nombre_de_la_imagen_gsi.img

# Borrado obligatorio de datos de usuario (Factory Reset)
fastboot -w

# Reiniciar el dispositivo en la nueva ROM
fastboot reboot</pre>

<p>4. El dispositivo iniciará la Custom ROM. El primer arranque puede tardar entre 3 y 7 minutos.</p>

---

<h2>4. Alternativa Recomendada sin Root: Debloat y Optimización Segura</h2>
<p>
Si no deseas correr el riesgo de desbloquear el bootloader o perder la tecnología NxtVision de las pantallas TCL, existe un método <strong>100% seguro</strong> para mejorar radicalmente el rendimiento, eliminar aplicaciones basura (bloatware) y maximizar la batería:
</p>

<ol>
  <li><strong>Universal Android Debloater Next Generation (UAD-ng):</strong>
    <ul>
      <li>Permite conectar el dispositivo por ADB sin necesidad de root.</li>
      <li>Desinstala de forma segura telemetría de TCL, apps duplicadas de operadores y servicios innecesarios en segundo plano a nivel de usuario (<code>pm uninstall -k --user 0</code>).</li>
      <li>Es reversible en cualquier momento con un clic.</li>
    </ul>
  </li>
  <li><strong>Shizuku:</strong>
    <ul>
      <li>Permite ejecutar aplicaciones que requieren privilegios elevados (como gestores de congelación de apps Hail, App Manager o gestores de copias de seguridad Neo Backup) mediante un servicio ADB que se activa por Wi-Fi o PC, sin modificar el kernel ni disparar las alarmas de seguridad bancaria.</li>
    </ul>
  </li>
</ol>

---

<h2>5. Directorio de Enlaces Oficiales de Descarga</h2>
<p>Todos los enlaces siguientes corresponden a los repositorios originales, verificados y libres de publicidad o malware:</p>

<table>
  <tr>
    <th>Herramienta / Software</th>
    <th>Descripción</th>
    <th>Enlace Oficial de Descarga</th>
  </tr>
  <tr>
    <td><strong>Magisk (Oficial)</strong></td>
    <td>Solución estándar de root para Android (por John Wu).</td>
    <td><a href="https://github.com/topjohnwu/Magisk/releases">github.com/topjohnwu/Magisk/releases</a></td>
  </tr>
  <tr>
    <td><strong>mtkclient</strong></td>
    <td>Herramienta de bajo nivel BROM para chipsets MediaTek (por B. Kerler).</td>
    <td><a href="https://github.com/bkerler/mtkclient">github.com/bkerler/mtkclient</a></td>
  </tr>
  <tr>
    <td><strong>Android SDK Platform-Tools</strong></td>
    <td>Binarios oficiales de ADB y Fastboot mantenidos por Google.</td>
    <td><a href="https://developer.android.com/tools/releases/platform-tools">developer.android.com/tools/releases/platform-tools</a></td>
  </tr>
  <tr>
    <td><strong>LineageOS GSI (AndyCGYan)</strong></td>
    <td>Compilaciones universales GSI de LineageOS (Android 13 / 14).</td>
    <td><a href="https://github.com/AndyCGYan/lineage_build_unified/releases">github.com/AndyCGYan/lineage_build_unified/releases</a></td>
  </tr>
  <tr>
    <td><strong>PixelOS GSI (Ponces)</strong></td>
    <td>Compilaciones GSI con la interfaz Pixel oficial de Google.</td>
    <td><a href="https://github.com/ponces/treble_build_pe/releases">github.com/ponces/treble_build_pe/releases</a></td>
  </tr>
  <tr>
    <td><strong>TrebleDroid AOSP GSI</strong></td>
    <td>Base universal AOSP de Project Treble (Phhusson / TrebleDroid).</td>
    <td><a href="https://github.com/TrebleDroid/treble_experimentations/releases">github.com/TrebleDroid/treble_experimentations/releases</a></td>
  </tr>
  <tr>
    <td><strong>crDroid GSI</strong></td>
    <td>ROM GSI altamente configurable basada en LineageOS.</td>
    <td><a href="https://github.com/Nazim/crdroid_gsi/releases">github.com/Nazim/crdroid_gsi/releases</a></td>
  </tr>
  <tr>
    <td><strong>LeOS GSI (Desgooglizada)</strong></td>
    <td>ROM GSI centrada exclusivamente en la privacidad y sin Google.</td>
    <td><a href="https://leos-gsi.de/">leos-gsi.de</a></td>
  </tr>
  <tr>
    <td><strong>Universal Android Debloater (UAD-ng)</strong></td>
    <td>Herramienta gráfica para desinstalar bloatware sin root mediante ADB.</td>
    <td><a href="https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation/releases">github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation/releases</a></td>
  </tr>
  <tr>
    <td><strong>Shizuku</strong></td>
    <td>Servicio para ejecutar APIs de sistema con privilegios ADB.</td>
    <td><a href="https://shizuku.rikka.app/">shizuku.rikka.app</a></td>
  </tr>
  <tr>
    <td><strong>Firmwares Oficiales TCL (Soporte)</strong></td>
    <td>Repositorio de firmwares stock para recuperación en caso de bootloop.</td>
    <td><a href="https://firmwarefile.com/tcl-40-se-t610k">firmwarefile.com/tcl-40-se-t610k</a></td>
  </tr>
</table>

<div class="footer">
  <p>Documento generado para el usuario <strong>bender</strong> en el entorno de trabajo Linux. Archivo fuente ODT listo para su visualización y edición en LibreOffice Writer.</p>
</div>

</body>
</html>
"""

html_path = "/home/bender/Descargas/manual_root_rom_tcl_40_se_y_tablets.html"
odt_path = "/home/bender/Descargas/manual_root_rom_tcl_40_se_y_tablets.odt"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado en {html_path}")

cmd = [
    "libreoffice",
    "--headless",
    "--convert-to", "odt",
    html_path,
    "--outdir", "/home/bender/Descargas"
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("Salida LibreOffice:", res.stdout)
if res.stderr:
    print("Error LibreOffice:", res.stderr)

if os.path.exists(odt_path):
    print(f"¡Éxito! Archivo ODT creado correctamente en: {odt_path} ({os.path.getsize(odt_path)} bytes)")
else:
    print("Error: No se encontró el archivo ODT.")
