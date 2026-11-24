#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

OUTPUT_HTML = "/tmp/manual_retroarch_xbox.html"
OUTPUT_ODT = "/home/bender/Descargas/Manual_RetroArch_Xbox_Instalacion_y_Compatibilidad.odt"

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Manual Técnico: Instalación de RetroArch en Xbox, Gestión de Núcleos y Tabla de Compatibilidad</title>
<style>
    @page {
        margin: 2cm;
    }
    body {
        font-family: 'Segoe UI', 'Liberation Sans', 'DejaVu Sans', Arial, sans-serif;
        line-height: 1.5;
        color: #222222;
        background-color: #FFFFFF;
        font-size: 10.5pt;
    }
    h1 {
        color: #107C10;
        font-size: 22pt;
        border-bottom: 3px solid #107C10;
        padding-bottom: 6px;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    h2 {
        color: #0E610E;
        font-size: 15pt;
        border-bottom: 1.5px solid #107C10;
        padding-bottom: 4px;
        margin-top: 22px;
        margin-bottom: 10px;
    }
    h3 {
        color: #1C355E;
        font-size: 12pt;
        margin-top: 15px;
        margin-bottom: 6px;
    }
    p {
        margin-top: 4px;
        margin-bottom: 8px;
        text-align: justify;
    }
    ul, ol {
        margin-top: 4px;
        margin-bottom: 8px;
        padding-left: 22px;
    }
    li {
        margin-bottom: 4px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 12px;
        margin-bottom: 15px;
        font-size: 9.5pt;
    }
    th {
        background-color: #107C10;
        color: #FFFFFF;
        padding: 8px 6px;
        text-align: left;
        border: 1px solid #0E610E;
    }
    td {
        padding: 6px;
        border: 1px solid #CCCCCC;
        vertical-align: top;
    }
    tr:nth-child(even) {
        background-color: #F8F9FA;
    }
    .badge-si {
        background-color: #D4EDDA;
        color: #155724;
        font-weight: bold;
        padding: 2px 5px;
        border-radius: 3px;
        display: inline-block;
    }
    .badge-ajustes {
        background-color: #FFF3CD;
        color: #856404;
        font-weight: bold;
        padding: 2px 5px;
        border-radius: 3px;
        display: inline-block;
    }
    .badge-app {
        background-color: #CCE5FF;
        color: #004085;
        font-weight: bold;
        padding: 2px 5px;
        border-radius: 3px;
        display: inline-block;
    }
    .note-box {
        background-color: #E8F5E9;
        border-left: 5px solid #107C10;
        padding: 10px 14px;
        margin: 12px 0;
        border-radius: 0 4px 4px 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 10px 14px;
        margin: 12px 0;
        border-radius: 0 4px 4px 0;
    }
    .danger-box {
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
        padding: 10px 14px;
        margin: 12px 0;
        border-radius: 0 4px 4px 0;
    }
    code {
        font-family: 'Consolas', 'Courier New', monospace;
        background-color: #F1F1F1;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 9.5pt;
        color: #B22222;
    }
    pre {
        background-color: #2D3748;
        color: #E2E8F0;
        padding: 10px;
        border-radius: 4px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        overflow-x: auto;
        line-height: 1.4;
    }
</style>
</head>
<body>

<h1>Manual Técnico: Instalación de RetroArch en Xbox, Gestión de Núcleos y Tabla de Compatibilidad</h1>
<p><strong>Ámbito:</strong> Consolas Xbox One, Xbox Series S y Xbox Series X en Modo Desarrollador (Developer Mode).<br>
<strong>Objetivo:</strong> Guía definitiva para descargar e instalar los paquetes oficiales de RetroArch UWP, gestionar sus núcleos sin provocar roturas del sistema, configurar los permisos de almacenamiento y consultar la compatibilidad por consolas.</p>

<hr>

<h2>1. Requisitos Previos y Modo Desarrollador (Developer Mode)</h2>
<p>Desde mediados de 2023, Microsoft clausuró los certificados que permitían ejecutar emuladores en el modo estándar (Retail Mode). Por tanto, la instalación de RetroArch se realiza de manera 100% legal y permanente mediante el <strong>Modo Desarrollador</strong>:</p>
<ul>
    <li><strong>Cuenta de desarrollador:</strong> Registro en el portal Microsoft Partner Center (pago único de tarifa de desarrollador de Microsoft).</li>
    <li><strong>App en la consola:</strong> Descargar la aplicación oficial <em>Xbox Dev Mode Activation</em> desde la Microsoft Store de la consola y vincular el código de 6 dígitos con la cuenta de desarrollador.</li>
    <li><strong>Reinicio en Developer Home:</strong> Al reiniciar, la consola arranca en el entorno Dev Home, mostrando su dirección IP local (por ejemplo, <code>192.168.1.50</code>) y el interruptor <em>Xbox Device Portal</em>.</li>
</ul>

<div class="note-box">
    <strong>Ventaja del Modo Desarrollador:</strong> No existe riesgo de baneo de consola ni de perfil de Xbox Live, ya que es el entorno oficial provisto por Microsoft para pruebas y desarrollo de software propio (UWP).
</div>

<h2>2. Cómo Descargar el Instalador Oficial de RetroArch para Xbox</h2>
<p>RetroArch en Xbox no es un instalador ejecutable tradicional (.exe), sino un paquete firmado para la <strong>Plataforma Universal de Windows (UWP)</strong> con extensión <code>.msixbundle</code> o <code>.appxbundle</code>.</p>

<h3>2.1. Fuentes Oficiales de Descarga</h3>
<ol>
    <li><strong>Página oficial de RetroArch:</strong>
        <ul>
            <li>Enlace oficial: <code>https://www.retroarch.com/?page=platforms</code></li>
            <li>En la sección de <strong>Xbox One / Xbox Series</strong>, descarga la versión <em>Stable</em> del paquete <code>RetroArch.msixbundle</code>.</li>
        </ul>
    </li>
    <li><strong>Servidor de compilaciones (Buildbot de Libretro):</strong>
        <ul>
            <li>URL: <code>https://buildbot.libretro.com/stable/</code> (navegar a la última versión disponible, subdirectorio <code>windows/msvc2019_uwp/x64/</code>).</li>
            <li>Aquí se descargan tanto las versiones estables consolidadas como las compilaciones <em>nightly</em> con mejoras recientes.</li>
        </ul>
    </li>
    <li><strong>Dependencia obligatoria de Microsoft (VCLibs):</strong>
        <ul>
            <li>RetroArch requiere las librerías de tiempo de ejecución de Visual C++ para UWP: <code>Microsoft.VCLibs.x64.14.00.appx</code>.</li>
            <li>Si no se instala esta dependencia junto con el paquete principal, Xbox Device Portal arrojará un error de instalación por falta de marco de dependencias (<em>Missing Framework Dependency</em>).</li>
        </ul>
    </li>
</ol>

<h3>2.2. Instalación Paso a Paso mediante Xbox Device Portal</h3>
<ol>
    <li>En la Xbox (dentro de Dev Home), asegúrate de que la casilla <strong>Enable Xbox Device Portal</strong> esté marcada. Toma nota de la URL HTTPS que aparece en pantalla y de las credenciales de usuario/contraseña si las configuraste.</li>
    <li>En tu ordenador (conectado a la misma red local), abre un navegador web y accede a <code>https://[IP_DE_TU_XBOX]:11443/</code> (acepta la advertencia de certificado autofirmado SSL).</li>
    <li>En el menú lateral izquierdo, haz clic en la sección <strong>Apps</strong>.</li>
    <li>Bajo el apartado <em>Deploy App</em>, pulsa en el botón <strong>Choose File</strong> y selecciona el archivo <code>RetroArch.msixbundle</code> descargado en tu ordenador.</li>
    <li>Haz clic en <strong>Next</strong>. El portal solicitará los paquetes de dependencias. Pulsa <em>Choose File</em> y adjunta el archivo <code>Microsoft.VCLibs.x64.14.00.appx</code>.</li>
    <li>Pulsa en <strong>Start</strong>. Espera a que la barra de progreso complete la subida y marque el estado <em>Success</em>.</li>
</ol>

<div class="danger-box">
    <strong>¡AJUSTE CRÍTICO OBLIGATORIO DE MEMORIA (APP vs GAME)!</strong><br>
    Por defecto, Xbox instala RetroArch con el perfil de <em>App</em> (aplicación básica de fondo). Bajo este perfil, la consola <strong>restringe la memoria a solo 1 GB de RAM</strong> y deshabilita la aceleración gráfica avanzada, provocando cierres inesperados al cargar juegos.<br><br>
    <strong>Solución en Xbox Device Portal:</strong>
    <ol>
        <li>En la lista de aplicaciones instaladas, localiza <strong>RetroArch</strong>.</li>
        <li>Haz clic en el menú desplegable de propiedades de la app o pulsa en <em>Actions</em>.</li>
        <li>Cambia el tipo de aplicación de <strong>App</strong> a <strong>Game</strong>.</li>
        <li>Esto desbloquea de inmediato más de <strong>5 GB de memoria RAM</strong> y permite el acceso completo a los núcleos de la CPU y la GPU.</li>
    </ol>
</div>

<h2>3. Cómo Descargar y Gestionar los Núcleos Oficiales Compatibles con Xbox</h2>

<p>Un error crítico común en Xbox es intentar instalar núcleos convencionales de Windows x86/x64 pensados para ordenadores de escritorio. En Xbox, los núcleos <strong>deben estar compilados específicamente para el conjunto de APIs de UWP (MSVC UWP x64)</strong>.</p>

<h3>3.1. Dónde se obtienen los núcleos UWP oficiales</h3>
<ul>
    <li><strong>Integrados en el paquete inicial:</strong> La gran ventaja del paquete <code>RetroArch.msixbundle</code> oficial para Xbox es que ya viene con una selección preinstalada de los núcleos más populares y estables optimizados para la consola.</li>
    <li><strong>Repositorio Buildbot UWP:</strong> Si necesitas un núcleo adicional o restaurar uno corrupto, visita:
        <br><code>https://buildbot.libretro.com/nightly/windows/msvc2019_uwp/x64/</code>
        <br>En este directorio encontrarás los archivos individuales con extensión <code>.dll</code> compilados estrictamente bajo el SDK de UWP.
    </li>
</ul>

<h3>3.2. Instalación manual de núcleos en la consola</h3>
<p>Para copiar archivos de núcleos (.dll) o archivos de opciones (.opt) a la Xbox, tienes dos métodos contrastados:</p>
<ol>
    <li><strong>Mediante el File Explorer de Xbox Device Portal:</strong>
        <ul>
            <li>En el menú lateral del Device Portal en tu PC, haz clic en <strong>File Explorer</strong>.</li>
            <li>Navega a la ruta: <code>DevelopmentFiles > WindowsApps > [Carpeta_RetroArch] > cores</code> o bien a <code>DevelopmentFiles > LocalState > cores</code>.</li>
            <li>Utiliza el botón <em>Upload File</em> para subir la DLL del núcleo deseado.</li>
        </ul>
    </li>
    <li><strong>Mediante Servidor FTP:</strong>
        <ul>
            <li>Instala y ejecuta la aplicación <em>Durango FTP</em> en tu Xbox Dev Mode, o activa el servidor FTP integrado en los ajustes de RetroArch.</li>
            <li>Conéctate desde tu PC con clientes como FileZilla apuntando a la IP de la consola por el puerto 21 para transferir archivos a gran velocidad.</li>
        </ul>
    </li>
</ol>

<div class="warning-box">
    <strong>¡PELIGRO CON EL ACTUALIZADOR EN LÍNEA DE RETROARCH EN XBOX!</strong><br>
    En la versión de PC con Linux o Windows, ir a <em>Actualizador en línea > Actualizador de núcleos</em> es seguro. <strong>En Xbox NO lo hagas a la ligera</strong>.<br>
    En numerosas ocasiones, el actualizador en línea interno descarga binarios de escritorio que sobreescriben los núcleos específicos de UWP, provocando que los juegos dejen de abrirse con el error <em>"Fallo en el núcleo"</em>.<br>
    <strong>Recomendación técnica:</strong> En <em>Ajustes > Menú principal > Actualizador en línea</em>, bloquea la descarga automática de núcleos para proteger la instalación estable.
</div>

<h2>4. La Clave de los Permisos NTFS: Cómo Evitar el "Error en el Contenido"</h2>
<p>Si conectas un pendrive o disco duro externo con tus juegos y BIOS a la Xbox y te arroja <em>"Error en el contenido"</em> tanto en Game Boy Color como en Game Boy Advance y Nintendo 64, el problema radica en los <strong>permisos de seguridad del sistema de archivos</strong>:</p>

<ol>
    <li>Conecta tu disco USB al PC con Windows. Debe tener formato <strong>NTFS</strong> (FAT32 y exFAT carecen de listas de control de acceso de seguridad).</li>
    <li>Abre el explorador de archivos, haz clic derecho sobre la unidad USB y pulsa <strong>Propiedades</strong>.</li>
    <li>Dirígete a la pestaña <strong>Seguridad</strong> y haz clic en el botón <strong>Opciones avanzadas</strong>.</li>
    <li>Pulsa en <strong>Agregar</strong> y luego en <strong>Seleccionar una entidad de seguridad</strong>.</li>
    <li>En el cuadro de texto escribe: <code>ALL APPLICATION PACKAGES</code> (en sistemas en español también se reconoce buscando en <em>Opciones avanzadas > Buscar ahora > TODOS LOS PAQUETES DE APLICACIONES</em>).</li>
    <li>Marca la casilla <strong>Control total</strong> y pulsa Aceptar.</li>
    <li>Marca la casilla inferior: <strong>"Reemplazar todas las entradas de permisos de objetos secundarios por entradas de permisos heredables de este objeto"</strong>.</li>
    <li>Pulsa <em>Aplicar</em> y <em>Aceptar</em>.</li>
    <li>Al conectar el USB a la Xbox, si aparece un menú preguntando para qué deseas usar la unidad, selecciona siempre <strong>Medios (Media)</strong>, nunca "Juegos y Aplicaciones".</li>
</ol>

<h2>5. Tabla Completa de Compatibilidad de Consolas y Sistemas en Xbox</h2>
<p>A continuación se detalla el estado real de compatibilidad de cada sistema emulado en consolas Xbox One y Xbox Series X|S, especificando el núcleo recomendado y si se requieren ajustes técnicos adicionales:</p>

<table>
    <thead>
        <tr>
            <th style="width: 20%;">Sistema / Consola</th>
            <th style="width: 18%;">¿Se puede jugar en Xbox?</th>
            <th style="width: 25%;">Núcleo o App Recomendada</th>
            <th style="width: 37%;">Ajustes Necesarios y Observaciones</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Game Boy / Game Boy Color (GB / GBC)</strong></td>
            <td><span class="badge-si">Sí (Perfecto)</span></td>
            <td><code>Gambatte</code><br>o <code>Gearboy</code></td>
            <td>Requiere permisos NTFS en el USB. No necesita BIOS externa (la emula internamente). Compatibilidad del 100% a 60 FPS estables.</td>
        </tr>
        <tr>
            <td><strong>Game Boy Advance (GBA)</strong></td>
            <td><span class="badge-si">Sí (Perfecto)</span></td>
            <td><code>mGBA</code><br>o <code>VBA Next</code></td>
            <td>Requiere permisos NTFS en el USB. Funciona sin BIOS mediante emulación HLE, aunque se recomienda colocar <code>gba_bios.bin</code> en la carpeta <code>system/</code> para eliminar pequeñas incompatibilidades de audio.</td>
        </tr>
        <tr>
            <td><strong>Nintendo 64 (N64)</strong></td>
            <td><span class="badge-ajustes">Sí (Con Ajustes)</span></td>
            <td><code>Mupen64Plus-Next</code><br>o <code>ParaLLEl N64</code></td>
            <td><strong>Requiere ajustes:</strong> Driver de vídeo en <code>d3d11</code>. Instalar el archivo de configuración <code>Mupen64Plus-Next.opt</code> con plugin gráfico compatible (GLideN64 adaptado o Angrylion multihilo por software) para evitar crasheos de DirectX.</td>
        </tr>
        <tr>
            <td><strong>NES / Famicom (8 bits)</strong></td>
            <td><span class="badge-si">Sí (Perfecto)</span></td>
            <td><code>Mesen</code><br>o <code>FCEUmm</code></td>
            <td>Rendimiento impecable sin necesidad de ajustes adicionales más allá de permisos de lectura de la ROM.</td>
        </tr>
        <tr>
            <td><strong>Super Nintendo (SNES)</strong></td>
            <td><span class="badge-si">Sí (Perfecto)</span></td>
            <td><code>Snes9x</code><br>o <code>bsnes</code></td>
            <td>Excelente precisión. Compatible con chips especiales (Super FX, SA-1). En consolas Xbox One base, <code>Snes9x</code> es la opción más ligera.</td>
        </tr>
        <tr>
            <td><strong>Nintendo DS (NDS)</strong></td>
            <td><span class="badge-si">Sí (Muy bueno)</span></td>
            <td><code>DeSmuME</code><br>o <code>MelonDS</code></td>
            <td><code>DeSmuME</code> arranca directamente sin archivos adicionales. <code>MelonDS</code> requiere los archivos <code>bios7.bin</code>, <code>bios9.bin</code> y <code>firmware.bin</code> en la carpeta <code>system/</code>. Mapear un botón del mando para alternar entre pantalla táctil y superior.</td>
        </tr>
        <tr>
            <td><strong>Nintendo GameCube y Wii</strong></td>
            <td><span class="badge-app">Sí (Vía App Dedicada)</span></td>
            <td><strong>Dolphin Xbox UWP</strong><br><em>(Standalone recomendado)</em></td>
            <td>Aunque existe el núcleo <code>dolphin_libretro</code>, la comunidad recomienda encarecidamente instalar la aplicación independiente <strong>Dolphin UWP</strong>. En Xbox Series S/X permite jugar a resolución 1080p y 4K con tasa de frames perfecta.</td>
        </tr>
        <tr>
            <td><strong>Sega Master System / Mega Drive / Genesis</strong></td>
            <td><span class="badge-si">Sí (Perfecto)</span></td>
            <td><code>Genesis Plus GX</code><br>o <code>PicoDrive</code></td>
            <td>Rendimiento total a 60 FPS sin configuraciones complejas. Para emulación de Sega CD, se requiere la BIOS correspondiente (<code>bios_CD_E.bin</code>, <code>bios_CD_U.bin</code>) en <code>system/</code>.</td>
        </tr>
        <tr>
            <td><strong>Sega Saturn</strong></td>
            <td><span class="badge-ajustes">Sí (Con Ajustes)</span></td>
            <td><code>Beetle Saturn</code><br>o <code>YabaSanshiro</code></td>
            <td>Exige situar las BIOS originales (<code>sega_101.bin</code> / <code>mpr-17933.bin</code>) en la carpeta <code>system/</code>. En Xbox One puede sufrir ralentizaciones; en Series S/X funciona con total fluidez.</td>
        </tr>
        <tr>
            <td><strong>Sega Dreamcast</strong></td>
            <td><span class="badge-si">Sí (Excelente)</span></td>
            <td><code>Flycast</code></td>
            <td>Requiere el archivo de BIOS <code>dc_boot.bin</code> en la subcarpeta <code>system/dc/</code>. El controlador de vídeo debe mantenerse en <code>d3d11</code> o <code>d3d12</code>.</td>
        </tr>
        <tr>
            <td><strong>Sony PlayStation 1 (PS1)</strong></td>
            <td><span class="badge-si">Sí (Perfecto)</span></td>
            <td><code>DuckStation</code><br>o <code>SwanStation</code></td>
            <td>Requiere BIOS oficiales (como <code>scph5501.bin</code> para región NTSC o <code>scph5502.bin</code> para PAL). Permite escalado de resolución a 1440p y corrección de texturas (PGXP).</td>
        </tr>
        <tr>
            <td><strong>Sony PlayStation 2 (PS2)</strong></td>
            <td><span class="badge-app">Sí (Vía App Dedicada)</span></td>
            <td><strong>XBSX2</strong><br><em>(Standalone recomendado)</em></td>
            <td>El núcleo interno de RetroArch (<code>LRPS2</code>) presenta cierres e inestabilidad en Xbox. El consenso unánime de la scene es instalar la app dedicada <strong>XBSX2</strong> (puerto UWP de PCSX2) en Dev Mode, la cual ejecuta prácticamente todo el catálogo de PS2 a 60 FPS en Xbox Series S/X. Requiere BIOS de PS2 en su directorio de datos.</td>
        </tr>
        <tr>
            <td><strong>Sony PlayStation Portable (PSP)</strong></td>
            <td><span class="badge-si">Sí (Excelente)</span></td>
            <td><code>PPSSPP</code></td>
            <td>Requiere descargar la carpeta de recursos de fuentes y activos (<em>assets</em>) de PPSSPP y colocarla en <code>system/PPSSPP/</code> para evitar textos invisibles en los menús. Gran rendimiento con reescalado a 1080p.</td>
        </tr>
        <tr>
            <td><strong>Arcade (Neo-Geo, Capcom CPS1/2/3, MAME)</strong></td>
            <td><span class="badge-si">Sí (Excelente)</span></td>
            <td><code>FinalBurn Neo (FBNeo)</code><br>o <code>MAME 2003-Plus</code></td>
            <td>Las ROMs deben coincidir exactamente con el ROMset que exige la versión del núcleo. Para juegos de Neo-Geo es obligatorio que el archivo <code>neogeo.zip</code> esté presente en el mismo directorio que los juegos o en <code>system/</code>.</td>
        </tr>
    </tbody>
</table>

<h2>6. Configuración de Directorios y Archivo de Optimización para N64</h2>
<p>Para asegurar que los juegos encuentren siempre sus archivos auxiliares sin depender de rutas rotas:</p>
<ol>
    <li>En RetroArch, ve a <strong>Ajustes > Directorios</strong>.</li>
    <li>Asegúrate de que la ruta de <strong>Sistema/BIOS</strong> apunte al almacenamiento local asignado de la consola:
        <br><code>S:\ProgramData\RetroArch\system</code> o <code>D:\DevelopmentFiles\WindowsApps\[RetroArch]\system</code>.</li>
    <li><strong>Instalación del archivo de opciones de N64:</strong>
        <br>Copia el archivo optimizado <code>Mupen64Plus-Next.opt</code> en la ruta:
        <br><code>LocalState/config/Mupen64Plus-Next/Mupen64Plus-Next.opt</code>
        <br>Este archivo desactiva los efectos de framebuffer que ahogan a la consola y fuerza un plugin compatible con la arquitectura DirectX de Xbox.</li>
</ol>

<hr>
<p style="text-align: center; font-size: 9pt; color: #666666;">
    Manual de Referencia Técnica - Scene de Emulación Xbox UWP - Generado para Uso Profesional
</p>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML escrito en {OUTPUT_HTML}")

# Convert to ODT with LibreOffice
cmd = ["libreoffice", "--headless", "--convert-to", "odt", OUTPUT_HTML, "--outdir", "/tmp"]
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if res.returncode == 0:
    tmp_odt = "/tmp/manual_retroarch_xbox.odt"
    if os.path.exists(tmp_odt):
        import shutil
        shutil.move(tmp_odt, OUTPUT_ODT)
        print(f"Éxito: Archivo ODT generado en {OUTPUT_ODT}")
        print(f"Tamaño: {os.path.getsize(OUTPUT_ODT)} bytes")
    else:
        print("Error: No se encontró el archivo ODT temporal.")
else:
    print(f"Error al ejecutar LibreOffice: {res.stderr.decode('utf-8')}")
