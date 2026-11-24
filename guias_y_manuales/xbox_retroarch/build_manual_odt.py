#!/usr/bin/env python3
import os
import sys
import shutil
import zipfile
import re

ASSETS_DIR = "/home/bender/Descargas/manual_xbox_assets"
HTML_PATH = "/tmp/manual_xbox.html"
FINAL_ODT = "/home/bender/Descargas/Manual_Xbox_Modo_Retail_y_Desarrollador.odt"

html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Manual: Transición entre Modo Retail y Modo Desarrollador en Xbox, Solución a Errores de N64, GBA, GBC y Guía de BIOS</title>
<style>
    @page {{
        margin: 2.5cm;
    }}
    body {{
        font-family: 'Segoe UI', 'Liberation Sans', 'DejaVu Sans', Arial, sans-serif;
        line-height: 1.6;
        color: #222222;
        background-color: #FFFFFF;
        font-size: 11pt;
    }}
    h1 {{
        color: #107C10;
        font-size: 24pt;
        border-bottom: 3px solid #107C10;
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 15px;
    }}
    h2 {{
        color: #0E610E;
        font-size: 17pt;
        border-bottom: 1px solid #D0D0D0;
        padding-bottom: 5px;
        margin-top: 25px;
        margin-bottom: 12px;
    }}
    h3 {{
        color: #1C355E;
        font-size: 13pt;
        margin-top: 18px;
        margin-bottom: 8px;
    }}
    h4 {{
        color: #D9381E;
        font-size: 11.5pt;
        margin-top: 14px;
        margin-bottom: 6px;
    }}
    p {{
        margin-bottom: 12px;
        text-align: justify;
    }}
    ul, ol {{
        margin-bottom: 14px;
        padding-left: 25px;
    }}
    li {{
        margin-bottom: 6px;
    }}
    .cover {{
        text-align: center;
        page-break-after: always;
        padding-top: 20px;
    }}
    .cover-title {{
        font-size: 24pt;
        font-weight: bold;
        color: #107C10;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .cover-subtitle {{
        font-size: 12pt;
        color: #444444;
        margin-bottom: 25px;
        font-style: italic;
    }}
    .cover-img {{
        width: 100%;
        max-width: 650px;
        border-radius: 8px;
        border: 2px solid #107C10;
        margin-bottom: 25px;
    }}
    .cover-meta {{
        font-size: 9.5pt;
        color: #666666;
        background-color: #F4F6F4;
        border: 1px solid #D8E2D8;
        border-radius: 6px;
        padding: 15px;
        max-width: 600px;
        margin: 0 auto;
        text-align: left;
    }}
    .figure-container {{
        text-align: center;
        margin: 22px 0;
        page-break-inside: avoid;
    }}
    .figure-img {{
        width: 100%;
        max-width: 620px;
        border: 1px solid #CCCCCC;
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }}
    .figure-caption {{
        font-size: 9.5pt;
        color: #555555;
        font-style: italic;
        margin-top: 6px;
    }}
    .callout {{
        border-left: 5px solid #107C10;
        background-color: #F0F8F0;
        padding: 12px 16px;
        margin: 16px 0;
        border-radius: 0 6px 6px 0;
    }}
    .callout-title {{
        font-weight: bold;
        color: #107C10;
        margin-bottom: 4px;
        font-size: 11pt;
    }}
    .warning {{
        border-left: 5px solid #D9381E;
        background-color: #FDF2F2;
        padding: 12px 16px;
        margin: 16px 0;
        border-radius: 0 6px 6px 0;
    }}
    .warning-title {{
        font-weight: bold;
        color: #D9381E;
        margin-bottom: 4px;
        font-size: 11pt;
    }}
    .tip {{
        border-left: 5px solid #0078D7;
        background-color: #F0F6FD;
        padding: 12px 16px;
        margin: 16px 0;
        border-radius: 0 6px 6px 0;
    }}
    .tip-title {{
        font-weight: bold;
        color: #0078D7;
        margin-bottom: 4px;
        font-size: 11pt;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 18px 0;
        font-size: 10pt;
    }}
    th, td {{
        border: 1px solid #CCCCCC;
        padding: 9px 12px;
        text-align: left;
    }}
    th {{
        background-color: #107C10;
        color: #FFFFFF;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #F9F9F9;
    }}
    code {{
        background-color: #EEEEEE;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Consolas', 'DejaVu Sans Mono', monospace;
        font-size: 9.5pt;
        color: #880000;
    }}
    .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 9pt;
        font-weight: bold;
    }}
    .badge-retail {{
        background-color: #D9EAF7;
        color: #0B5394;
    }}
    .badge-dev {{
        background-color: #D7F2D7;
        color: #107C10;
    }}
    .badge-error {{
        background-color: #F8D7DA;
        color: #721C24;
    }}
</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover">
    <div class="cover-title">Manual de Operación Xbox</div>
    <div class="cover-subtitle">Transición Bidireccional: Modo Retail ⟷ Modo Desarrollador (Developer Mode),<br>Solución a Errores 0x8027025a, N64, Game Boy Advance y Game Boy Color (Wario Land 3),<br>y Guía Maestra de Carga de BIOS en RetroArch (Pendrive vs Memoria Interna)</div>
    
    <img src="{ASSETS_DIR}/cover.jpg" class="cover-img" alt="Xbox Series X Dev Mode Setup">
    
    <div class="cover-meta">
        <strong>Plataformas compatibles:</strong> Xbox One, Xbox One S, Xbox One X, Xbox Series S, Xbox Series X<br>
        <strong>Método:</strong> Oficial de Microsoft (Universal Windows Platform - UWP)<br>
        <strong>Garantía:</strong> 100% Intacta (Sin modificaciones físicas ni alteración de firmware)<br>
        <strong>Secciones Especiales:</strong> Protocolo contra el error 0x8027025a, reparación de fallos de núcleo en Nintendo 64, Game Boy Advance y Game Boy Color (caso Wario Land 3), y análisis técnico comparativo de carga de BIOS de consolas.<br>
        <strong>Fecha de edición:</strong> Noviembre 2026
    </div>
</div>

<hr style="page-break-after:always; visibility:hidden;">

<!-- TABLA DE CONTENIDOS -->
<h2>Tabla de Contenidos</h2>
<ol>
    <li><strong>Introducción y Arquitectura de la Consola</strong>
        <ul>
            <li>¿Qué es el Modo Retail y el Modo Desarrollador?</li>
            <li>Aislamiento por Sandbox y Garantía de Hardware</li>
            <li>Esquema Conceptual del Flujo Bidireccional</li>
        </ul>
    </li>
    <li><strong>Requisitos Previos</strong>
        <ul>
            <li>Hardware y Almacenamiento Necesario</li>
            <li>Cuenta de Desarrollador en Microsoft Partner Center</li>
        </ul>
    </li>
    <li><strong>Fase 1: Preparación y Activación Inicial</strong>
        <ul>
            <li>Paso 1: Configuración en el portal web de Partner Center</li>
            <li>Paso 2: Instalación de la app oficial "Xbox Dev Mode"</li>
            <li>Paso 3: Vinculación con el código de 6 caracteres</li>
        </ul>
    </li>
    <li><strong>Fase 2: Pasar de Modo Retail a Modo Desarrollador (Retail ➔ Dev)</strong>
        <ul>
            <li>Paso 4: Ejecución del botón "Switch and restart"</li>
            <li>Paso 5: El entorno Dev Home y herramientas esenciales</li>
        </ul>
    </li>
    <li><strong>Fase 3: Volver de Modo Desarrollador a Modo Retail (Dev ➔ Retail)</strong>
        <ul>
            <li>Paso 6: Salir del modo Dev mediante "Leave Dev Mode"</li>
            <li><strong>¡Paso Crítico!:</strong> La casilla "Delete sideloaded games and apps"</li>
            <li>Paso 7: Retorno seguro al Dashboard estándar de juegos</li>
        </ul>
    </li>
    <li><strong>Fase 4: Ciclo Habitual en el Día a Día (Resumen Rápido)</strong></li>
    <li><strong>Fase 5: Diagnóstico y Solución Integral del Error 0x8027025a</strong>
        <ul>
            <li>¿Qué significa el error 0x8027025a y por qué ocurre?</li>
            <li>Solución 1: Cierre Forzado de la Aplicación Bloqueada (Force Quit)</li>
            <li>Solución 2: Ciclo de Energía Completo y Vaciado de Caché (Hard Reset / Power Cycle)</li>
            <li>Solución 3: Comprobación de Red y Conflictos de Perfiles</li>
            <li>Solución 4: Gestión y Permisos de Almacenamiento Externo USB</li>
            <li>Solución 5: Restablecimiento del Sistema Manteniendo Juegos y Aplicaciones (Soft Reset)</li>
        </ul>
    </li>
    <li><strong>Fase 6: Solución a Errores de Nintendo 64 en RetroArch ("Error en el contenido" y "Fallo en el núcleo")</strong>
        <ul>
            <li>Diagnóstico Técnico: ¿Por qué fallan Mupen64Plus-Next y ParaLLEl N64 en Xbox UWP?</li>
            <li>Paso 1: Configurar RetroArch como 'Game' en lugar de 'App' en Dev Home (Paso Clave e Imprescindible)</li>
            <li>Paso 2: Ajustar el Controlador de Vídeo a 'd3d11' en RetroArch</li>
            <li>Paso 3: Selección de Núcleo y Configuración de Plugins Gráficos (GLideN64 vs Angrylion)</li>
            <li>Paso 4: Descompresión de ROMs (.z64 / .n64 / .v64) y Permisos de la Unidad USB E:\</li>
            <li>Paso 5: Archivo de Rescate de Configuración (mupen64plus-next.opt)</li>
            <li>Paso 6: Actualización de Core Info Files y Prevención de Núcleos Rotos</li>
        </ul>
    </li>
    <li><strong>Fase 7: Guía Maestra de Carga de BIOS en RetroArch (Pendrive USB vs Memoria Interna)</strong>
        <ul>
            <li>¿Qué es una BIOS y qué consolas la requieren obligatoriamente?</li>
            <li>¿Es mejor cargarlas en el Pendrive USB o en la Memoria Interna? (Análisis Técnico)</li>
            <li>Estructura de Carpetas Recomendada en el Pendrive (E:\RetroArch\system\)</li>
            <li>Paso a Paso: Cómo configurar RetroArch para leer las BIOS desde el Pendrive</li>
            <li>Comprobación de Estado: Menú de Información del Núcleo ("Presente" vs "Ausente")</li>
            <li>Tabla Maestra de BIOS por Consola (Rutas, Nombres Exactos y Sensibilidad a Mayúsculas)</li>
        </ul>
    </li>
    <li><strong>Fase 8: Solución al Error de Game Boy Advance (GBA): "Error en el contenido / No se puede cargar"</strong>
        <ul>
            <li>Diagnóstico Técnico: ¿Por qué falla GBA incluso con la ruta de la BIOS seleccionada?</li>
            <li>Causa 1: Archivo de BIOS corrupto o tamaño incorrecto (El estándar de los 16.384 bytes)</li>
            <li>Causa 2: Choque con el núcleo gpSP y por qué debes cambiar a mGBA o VBA Next</li>
            <li>Causa 3: ROMs comprimidas en .zip/.7z y caracteres especiales en los nombres</li>
            <li>Causa 4: Permisos de escritura NTFS para los archivos de guardado (.srm / .sav)</li>
            <li>Protocolo de Solución Rápida en 4 Pasos (incluyendo rescate con BIOS HLE interna de mGBA)</li>
        </ul>
    </li>
    <li><strong>Fase 9: Solución al Error de Game Boy Color (GBC): Caso Real "Wario Land 3" y Fallos de Carga</strong>
        <ul>
            <li>Diagnóstico Técnico: ¿Por qué falla Wario Land 3 en RetroArch Xbox?</li>
            <li>Causa 1: Intento de cargar la ROM con núcleos incompatibles de GBA (como gpSP)</li>
            <li>Causa 2: Particularidad de Wario Land 3 (Chip MBC3 + Reloj en Tiempo Real RTC y guardado SRAM)</li>
            <li>Causa 3: Conflicto con la BIOS opcional de GBC (gbc_bios.bin de 2 KB) frente a Gambatte</li>
            <li>Causa 4: Compresión en .zip/.7z y permisos de escritura en la unidad E:\</li>
            <li>Protocolo de Solución Paso a Paso: Núcleo Gambatte, extracción .gbc y gestión de saves</li>
        </ul>
    </li>
    <li><strong>Fase 10: Otras Preguntas Frecuentes y Solución de Problemas Generales</strong></li>
    <li><strong>Fase 11: Tabla Comparativa y Resumen de Accesos</strong></li>
</ol>

<hr>

<!-- CAPÍTULO 1 -->
<h2>1. Introducción y Arquitectura de la Consola</h2>
<p>
Las consolas modernas de Microsoft (familia <strong>Xbox One</strong> y <strong>Xbox Series X|S</strong>) cuentan con una arquitectura de sistema operativo modular basada en Hyper-V. Esto permite que una consola comercial estándar adquirida en cualquier tienda pueda alternar de forma nativa entre dos entornos de ejecución completamente independientes:
</p>

<ul>
    <li><span class="badge badge-retail">MODO RETAIL</span> <strong>(Modo Tienda o Comercial):</strong> Es el estado predeterminado de fábrica. En este modo puedes jugar a todos tus títulos en disco o digitales, utilizar las suscripciones a <em>Xbox Game Pass</em>, acceder a Xbox Network, jugar multijugador online con matchmaking oficial y acumular logros. Por motivos de seguridad y antipiratería, este entorno bloquea cualquier código no firmado.</li>
    <li><span class="badge badge-dev">MODO DESARROLLADOR</span> <strong>(Developer Mode):</strong> Es un entorno sandbox de desarrollo UWP (Universal Windows Platform). Permite desplegar y probar aplicaciones propias, herramientas de diagnóstico, centros multimedia (como Kodi) y emuladores (como RetroArch o emuladores independientes). En este modo <strong>no se pueden ejecutar juegos comerciales de retail</strong> ni se accede al matchmaking de juegos de tienda, garantizando el aislamiento de seguridad.</li>
</ul>

<div class="callout">
    <div class="callout-title">✓ Seguridad y Garantía 100% Oficial</div>
    El Modo Desarrollador es una función oficial implementada por Microsoft para facilitar la creación de videojuegos independientes (ID@Xbox) y software educativo. <strong>No requiere modificar el hardware, no abre vulnerabilidades, no anula la garantía oficial del fabricante ni expone tu consola o perfil a baneos</strong> en Xbox Network siempre que se utilice siguiendo este manual.
</div>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img1_flujo_modos.png" class="figure-img" alt="Diagrama de flujo entre Modo Retail y Modo Desarrollador">
    <div class="figure-caption">Figura 1: Arquitectura de doble entorno en Xbox y ciclo de transición bidireccional.</div>
</div>

<hr>

<!-- CAPÍTULO 2 -->
<h2>2. Requisitos Previos</h2>
<p>Antes de iniciar el procedimiento, asegúrate de disponer de los siguientes elementos:</p>
<ol>
    <li><strong>Consola Xbox compatible:</strong> Cualquier modelo de Xbox One (Original, S, X) o Xbox Series (S, X) actualizado a la versión más reciente del sistema operativo.</li>
    <li><strong>Cuenta Microsoft:</strong> Una cuenta estándar de Microsoft (Outlook, Hotmail o cuenta personal vinculada a Xbox).</li>
    <li><strong>Registro en Microsoft Partner Center:</strong> Es necesario registrar una cuenta de desarrollador individual en el portal oficial de Microsoft. Este trámite tiene un <strong>coste único aproximado de 14 € / 19 $</strong> (pago único vitalicio; nunca caduca ni requiere suscripciones mensuales).</li>
    <li><strong>Almacenamiento interno disponible:</strong> Al menos <strong>20 a 30 GB</strong> de espacio libre en el disco interno de la consola para reservar la partición aislada de desarrollo.</li>
    <li><strong>Conexión a Internet:</strong> Conexión por cable Ethernet o Wi-Fi estable tanto en la consola como en el PC/móvil utilizado para la activación.</li>
</ol>

<hr>

<!-- CAPÍTULO 3 -->
<h2>3. Fase 1: Preparación y Activación Inicial</h2>

<h3>Paso 1: Registro en Microsoft Partner Center</h3>
<p>
Para autorizar a tu consola como dispositivo de desarrollo, debes acceder desde un ordenador o dispositivo móvil a la web oficial de Microsoft:
</p>
<ol>
    <li>Visita <a href="https://partner.microsoft.com/xboxconfig/devices">partner.microsoft.com/xboxconfig/devices</a> (o mediante el enlace directo <a href="https://aka.ms/activatexbox">aka.ms/activatexbox</a>).</li>
    <li>Inicia sesión con tu cuenta de Microsoft registrada como desarrollador.</li>
    <li>La página mostrará la sección <strong>"Manage Xbox One &amp; Series Consoles"</strong> con el campo preparado para introducir el código de activación que generará tu consola.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img2_partner_center.png" class="figure-img" alt="Portal web de Microsoft Partner Center">
    <div class="figure-caption">Figura 2: Portal de administración de consolas Xbox en Microsoft Partner Center.</div>
</div>

<h3>Paso 2: Instalación de la Aplicación Oficial en la Consola</h3>
<p>
En tu Xbox (estando en Modo Retail normal):
</p>
<ol>
    <li>Abre la aplicación <strong>Microsoft Store</strong> desde la pantalla de inicio.</li>
    <li>En la barra de búsqueda superior, escribe <code>Xbox Dev Mode</code> (o <code>Dev Mode Activation</code>).</li>
    <li>Selecciona la aplicación oficial publicada por <em>Microsoft Corporation</em>.</li>
    <li>Pulsa el botón <strong>"Obtener / Instalar"</strong> (la aplicación es 100% gratuita).</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img3_xbox_store_search.png" class="figure-img" alt="Descarga de Xbox Dev Mode en Microsoft Store">
    <div class="figure-caption">Figura 3: Instalación de la aplicación Xbox Dev Mode en la tienda oficial.</div>
</div>

<h3>Paso 3: Obtención e Introducción del Código de Activación</h3>
<p>
Una vez descargada la aplicación:
</p>
<ol>
    <li>Ejecuta la app <strong>Xbox Dev Mode</strong> en la consola.</li>
    <li>Aparecerá una pantalla de bienvenida que generará un <strong>código alfanumérico único de 6 caracteres</strong> (por ejemplo: <code>X7K2-9B</code>).</li>
    <li>Desde tu PC o teléfono, introduce dicho código en la página <a href="https://aka.ms/activatexbox">aka.ms/activatexbox</a> y haz clic en <strong>"Agree and activate"</strong>.</li>
    <li>En unos segundos, la pantalla de tu televisor detectará la vinculación y mostrará un mensaje de confirmación exitosa.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img4_dev_mode_activation_code.png" class="figure-img" alt="Pantalla de código en Xbox Dev Mode">
    <div class="figure-caption">Figura 4: Código alfanumérico de vinculación en la app de la consola.</div>
</div>

<hr>

<!-- CAPÍTULO 4 -->
<h2>4. Fase 2: Pasar de Modo Retail a Modo Desarrollador (Retail ➔ Dev)</h2>

<h3>Paso 4: El botón "Switch and restart"</h3>
<p>
Una vez completada la activación (o siempre que te encuentres en Modo Retail y desees pasar a Modo Desarrollador):
</p>
<ol>
    <li>Abre la aplicación <strong>Xbox Dev Mode</strong> desde tu biblioteca de juegos y aplicaciones.</li>
    <li>En la pantalla principal de la app, selecciona el botón verde central: <strong>"Switch and restart"</strong> (Cambiar y reiniciar).</li>
    <li>Confirma presionando el botón <strong>[A]</strong> de tu mando.</li>
    <li>La consola procederá a reiniciarse.</li>
</ol>

<div class="tip">
    <div class="tip-title">ℹ Tiempo de reinicio en el primer acceso</div>
    La primera vez que la consola arranca en Modo Desarrollador, el sistema tardará entre <strong>2 y 5 minutos</strong>, ya que formatea internamente la partición de desarrollo e inicializa los servicios de sandbox. En los arranques posteriores, el reinicio tardará prácticamente lo mismo que un encendido convencional.
</div>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img5_switch_and_restart.png" class="figure-img" alt="Pantalla Switch and restart">
    <div class="figure-caption">Figura 5: Botón 'Switch and restart' para iniciar el reinicio hacia Modo Desarrollador.</div>
</div>

<h3>Paso 5: El Entorno "Dev Home"</h3>
<p>
Cuando la consola termine de encenderse, verás una interfaz diferente: el panel <strong>Dev Home</strong>.
</p>
<p>
Este es el escritorio principal de desarrollo de Xbox. En él encontrarás las siguientes secciones fundamentales:
</p>
<ul>
    <li><strong>Barra de Estado Superior:</strong> Muestra el modo activo, la dirección IP local de la consola (por ejemplo, <code>192.168.1.85</code>) y el espacio de almacenamiento disponible.</li>
    <li><strong>Xbox Device Portal:</strong> Muestra la dirección web local (por ejemplo, <code>https://192.168.1.85:11443</code>). Al abrir esa dirección en el navegador web de tu PC, podrás subir archivos, instalar emuladores o paquetes <code>.msixbundle</code> / <code>.appx</code> de forma inalámbrica.</li>
    <li><strong>Panel Quick Actions (Acciones Rápidas):</strong> En la columna izquierda, con las opciones de apagado, reinicio y el botón para volver a Retail.</li>
    <li><strong>Development Games &amp; Apps:</strong> El mosaico donde se listan todas las aplicaciones instaladas en este modo.</li>
</ul>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img6_dev_home_dashboard.png" class="figure-img" alt="Dashboard Dev Home en Modo Desarrollador">
    <div class="figure-caption">Figura 6: Interfaz principal de Dev Home y herramientas de desarrollo.</div>
</div>

<div class="callout">
    <div class="callout-title">📡 Nota sobre la conexión Wi-Fi en Dev Mode</div>
    El Modo Retail y el Modo Desarrollador mantienen perfiles de red independientes. Si utilizas Wi-Fi en lugar de cable, es posible que la primera vez que entres en Dev Mode debas ir a <em>Configuración de Red</em> y volver a ingresar tu contraseña de Wi-Fi.
</div>

<hr>

<!-- CAPÍTULO 5 -->
<h2>5. Fase 3: Volver de Modo Desarrollador a Modo Retail (Dev ➔ Retail)</h2>

<p>
Cuando hayas terminado de probar tus aplicaciones o jugar a tus emuladores y quieras volver a jugar a tus juegos habituales de Xbox, charlar en grupos con amigos o utilizar Xbox Game Pass, debes realizar el proceso inverso para regresar al Modo Retail.
</p>

<h3>Paso 6: Seleccionar "Leave Dev Mode"</h3>
<ol>
    <li>En la pantalla de <strong>Dev Home</strong>, dirígete a la columna izquierda bajo la sección <strong>Quick Actions</strong> (Acciones Rápidas).</li>
    <li>Selecciona la opción destacada: <strong>"Leave Dev Mode"</strong> (Salir del modo Dev) y pulsa <strong>[A]</strong>.</li>
</ol>

<h3>Paso Crítico: El Cuadro de Confirmación y la Casilla de Seguridad</h3>
<p>
Al pulsar "Leave Dev Mode", aparecerá una ventana modal en el centro de la pantalla preguntando si deseas reiniciar la consola.
</p>

<div class="warning">
    <div class="warning-title">⚠️ ¡ADVERTENCIA CRÍTICA: NO MARCAR ESTA CASILLA!</div>
    En la ventana emergente verás la siguiente opción acompañada de una casilla de verificación:<br>
    <center style="margin: 8px 0; font-size: 11pt;"><code>[ ] Delete sideloaded games and apps</code></center>
    <strong>DEBES DEJAR ESTA CASILLA COMPLETAMENTE DESMARCADA (VACÍA).</strong><br><br>
    • <strong>Si la dejas DESMARCADA (Correcto):</strong> El sistema reiniciará la consola en Retail, pero conservará intactas todas tus aplicaciones, emuladores (RetroArch, etc.), partidas guardadas y configuraciones para cuando decidas regresar.<br>
    • <strong>Si la MARCAS (Incorrecto):</strong> La consola borrará por completo todos los programas y archivos que hayas instalado en la partición de desarrollo.
</div>

<p>
Una vez te hayas asegurado de que la casilla está <strong>desmarcada</strong>, sitúa el foco en el botón <strong>"Restart now"</strong> (Reiniciar ahora) y pulsa <strong>[A]</strong> en tu mando.
</p>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img7_leave_dev_mode_dialog.png" class="figure-img" alt="Diálogo de Leave Dev Mode con la casilla desmarcada">
    <div class="figure-caption">Figura 7: Ventana crítica de confirmación. La casilla debe permanecer sin marcar para no perder datos.</div>
</div>

<h3>Paso 7: Retorno Seguro al Dashboard Estándar</h3>
<p>
La consola se reiniciará y volverá a mostrar el Dashboard original de Xbox:
</p>
<ul>
    <li>Tus juegos comerciales (Halo, Forza, EA Sports FC, Call of Duty, etc.) funcionarán con total normalidad.</li>
    <li>El acceso a servidores multijugador, chat de voz y logros estará 100% activo.</li>
    <li>La aplicación <strong>Xbox Dev Mode</strong> permanecerá en tu biblioteca lista para cuando desees volver a cambiar de entorno.</li>
</ul>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img8_regreso_retail.png" class="figure-img" alt="Retorno al Dashboard habitual de Xbox en Retail">
    <div class="figure-caption">Figura 8: Dashboard comercial habitual con la aplicación Xbox Dev Mode disponible en la biblioteca.</div>
</div>

<hr>

<!-- CAPÍTULO 6 -->
<h2>6. Fase 4: Ciclo Habitual en el Día a Día (Resumen Rápido)</h2>

<p>
Una vez realizada la activación inicial por primera vez, el cambio entre ambos modos en el día a día se reduce a dos sencillos pasos que tardan menos de un minuto:
</p>

<table>
    <tr>
        <th>Operación</th>
        <th>Dónde se realiza</th>
        <th>Acción exacta a ejecutar</th>
    </tr>
    <tr>
        <td><strong>Ir de Retail ➔ Dev Mode</strong></td>
        <td>En Modo Retail (Dashboard estándar)</td>
        <td>Abrir la app <code>Xbox Dev Mode</code> ➔ Pulsar <strong>"Switch and restart"</strong>.</td>
    </tr>
    <tr>
        <td><strong>Volver de Dev Mode ➔ Retail</strong></td>
        <td>En Modo Dev (Pantalla Dev Home)</td>
        <td>En Quick Actions, pulsar <strong>"Leave Dev Mode"</strong> ➔ Dejar casilla vacía ➔ Pulsar <strong>"Restart now"</strong>.</td>
    </tr>
</table>

<hr>

<!-- CAPÍTULO 7: ERROR 0x8027025a DETALLADO -->
<h2>7. Fase 5: Diagnóstico y Solución Integral del Error 0x8027025a</h2>

<p>
Uno de los fallos más frecuentes reportados por los usuarios al utilizar el Modo Desarrollador, abrir la aplicación <strong>Xbox Dev Mode</strong> o lanzar emuladores y juegos es el <strong>código de error 0x8027025a</strong>.
</p>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img9_error_0x8027025a.png" class="figure-img" alt="Pantalla de error 0x8027025a en Xbox">
    <div class="figure-caption">Figura 9: Pantalla oficial del error 0x8027025a ("Vuelve a intentarlo / Tardó demasiado tiempo en iniciarse").</div>
</div>

<h3>¿Qué significa este error y por qué ocurre al cambiar de modo?</h3>
<p>
El código <code>0x8027025a</code> es un <strong>error de tiempo de espera agotado (Timeout)</strong> generado por el gestor de procesos del sistema operativo de Xbox. Cuando seleccionas una aplicación, el sistema le concede un intervalo de aproximadamente 20 a 30 segundos para cargar sus dependencias en memoria RAM y responder al hilo principal. Si no responde dentro de ese límite, el sistema suspende el inicio y lanza este error.
</p>
<p>
En el contexto específico de la transición entre <strong>Retail y Dev Mode</strong>, este error suele ocurrir por cuatro motivos concretos:
</p>
<ol>
    <li><strong>Saturación de la caché volátil:</strong> El modo de energía rápida ("Instant-On" o "Suspensión") almacena estados previos del sistema en memoria. Al pasar de un entorno a otro, hilos del sandbox anterior pueden quedarse en conflicto.</li>
    <li><strong>Proceso zombi en segundo plano:</strong> La app <em>Xbox Dev Mode</em> intentó inicializarse pero quedó en espera de un servicio de red que no respondió inmediatamente.</li>
    <li><strong>Fallo de autenticación temporal de Xbox Live:</strong> Al abrir una aplicación, la consola verifica licencias contra los servidores de Microsoft. Si la red Wi-Fi aún no ha negociado la IP tras el reinicio, la app se congela esperando respuesta.</li>
    <li><strong>Almacenamiento externo USB saturado:</strong> Si tienes configurado un disco externo USB para tus apps de desarrollo y no ha completado el montaje o tiene sectores lentos.</li>
</ol>

<hr>

<h3>Solución Progresiva Paso a Paso</h3>
<p>
Aplica las siguientes soluciones en orden, de la más rápida a la más profunda.
</p>

<h4>Solución 1: Cierre Forzado de la Aplicación Bloqueada (Force Quit)</h4>
<p>
Si la app se quedó congelada en segundo plano, forzar su terminación liberará la memoria asignada:
</p>
<ol>
    <li>Presiona el <strong>botón Xbox</strong> (la esfera luminosa central) en tu mando para desplegar la <strong>Guía</strong>.</li>
    <li>En la lista de aplicaciones recientes, sitúa el cursor sobre <strong>Xbox Dev Mode</strong> (o la app que está fallando).</li>
    <li>Presiona el <strong>botón Menú</strong> de tu mando (el botón con las tres líneas horizontales ☰).</li>
    <li>En el menú contextual emergente, selecciona la opción <strong>"Salir" (Quit)</strong> y pulsa <strong>[A]</strong>.</li>
    <li><strong>Espera 10 segundos</strong> completos para que el kernel libere los recursos en RAM.</li>
    <li>Vuelve a abrir la aplicación. En un 40% de los casos, la app arrancará correctamente de inmediato.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img10_solucion1_force_quit.png" class="figure-img" alt="Cierre forzado de la app desde la Guía de Xbox">
    <div class="figure-caption">Figura 10: Forzar el cierre de la app colgada mediante el botón Menú ➔ Salir.</div>
</div>

<hr>

<h4>Solución 2: Ciclo de Energía Completo y Vaciado de Caché (Power Cycle / Hard Reset)</h4>
<p>
Si el cierre forzado no resuelve el problema, significa que hay caché corrupta en el subsistema de la consola. El reinicio normal por software no vacía esta memoria; es necesario ejecutar un <strong>Power Cycle completo por hardware</strong>:
</p>
<ol>
    <li><strong>Apagado forzado:</strong> Con la consola encendida, mantén presionado el <strong>botón físico de encendido Xbox</strong> en el frontal de la consola durante <strong>10 segundos completos</strong>. Escucharás cómo los ventiladores y el disco se apagan por completo.</li>
    <li><strong>Drenaje de energía:</strong> Desconecta el <strong>cable de alimentación</strong> de la parte trasera de la consola de la corriente eléctrica.</li>
    <li><strong>Espera obligatoria:</strong> Espera entre <strong>30 y 60 segundos</strong>. Este tiempo es indispensable para que los condensadores de la placa base se descarguen y la memoria caché volátil se limpie por completo.</li>
    <li><strong>Reconexión y encendido:</strong> Vuelve a conectar el cable de alimentación y enciende la consola desde el botón frontal. Verás la animación completa de arranque de Xbox (pantalla verde o negra de inicio), confirmando que se ha realizado un inicio en frío.</li>
    <li>Abre nuevamente la aplicación <em>Xbox Dev Mode</em>.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img11_solucion2_power_cycle.png" class="figure-img" alt="Procedimiento de Power Cycle de 10 segundos">
    <div class="figure-caption">Figura 11: Secuencia física de Power Cycle para vaciar la memoria y reparar el error de tiempo de espera.</div>
</div>

<div class="callout">
    <div class="callout-title">✓ Efectividad Comprobada</div>
    El método de Power Cycle resuelve más del <strong>85% de las incidencias del error 0x8027025a</strong> provocadas por conflictos entre el Modo Suspensión y el arranque del sandbox de desarrollo.
</div>

<hr>

<h4>Solución 3: Comprobación de Red y Conflictos de Perfiles</h4>
<p>
Si el error persiste, la app puede estar bloqueada esperando respuesta del servicio de red:
</p>
<ul>
    <li><strong>Verificar estado de Xbox Network:</strong> Desde tu móvil o PC, consulta <a href="https://support.xbox.com/xbox-live-status">support.xbox.com/xbox-live-status</a> para confirmar que no haya caídas en los servicios de "Cuentas y perfiles" o "Tienda y suscripciones". Si hay alertas rojas, el timeout se debe a los servidores de Microsoft.</li>
    <li><strong>Reconexión de Red:</strong> Ve a <em>Configuración ➔ General ➔ Configuración de red ➔ Probar conexión de red</em>. Si estás en Dev Mode y utilizas Wi-Fi, asegúrate de que la consola se haya autenticado correctamente en tu router tras el reinicio.</li>
    <li><strong>Cerrar e iniciar sesión de perfil:</strong> En la Guía de Xbox, ve a la pestaña de perfil, selecciona <em>Cerrar sesión</em> y vuelve a iniciar sesión con tu cuenta de Microsoft. Esto refresca los tokens de seguridad OAuth de la cuenta de desarrollador.</li>
</ul>

<hr>

<h4>Solución 4: Desconexión de Dispositivos de Almacenamiento Externo USB</h4>
<p>
Si utilizas un disco duro externo o pendrive USB formateado para guardar tus ROMs o juegos de desarrollo:
</p>
<ol>
    <li>Apaga la consola y desconecta todos los discos duros externos, pendrives o concentradores USB.</li>
    <li>Enciende la consola con solo el mando conectado.</li>
    <li>Intenta abrir la aplicación <em>Xbox Dev Mode</em>.</li>
    <li>Si la app abre con normalidad sin el disco externo, el fallo se debe a que la unidad USB tiene sectores defectuosos, un sistema de archivos dañado o una velocidad de lectura insuficiente que bloquea la verificación inicial del sistema. Conecta el disco a un PC para ejecutar un análisis con <code>chkdsk</code>.</li>
</ol>

<hr>

<h4>Solución 5: Restablecimiento del Sistema Manteniendo Juegos y Aplicaciones (Soft Reset)</h4>
<p>
Si tras aplicar los pasos anteriores la aplicación sigue arrojando el error <code>0x8027025a</code> de forma indefinida, significa que los archivos del sistema operativo de Xbox sufrieron una corrupción en los registros de arranque.
</p>
<p>
La solución definitiva recomendada por el soporte oficial de Microsoft es realizar un <strong>Soft Reset</strong> (Restablecimiento suave):
</p>
<ol>
    <li>Presiona el botón Xbox del mando y ve a <strong>Configuración</strong> (el icono de engranaje).</li>
    <li>Navega a <strong>Sistema ➔ Información de la consola</strong>.</li>
    <li>Selecciona la opción <strong>"Restablecer consola"</strong> (Reset console).</li>
    <li>Aparecerán dos opciones críticas en pantalla:
        <ul>
            <li><strong style="color: #107C10;">"Restablecer y mantener mis juegos y aplicaciones" (OPCIÓN CORRECTA Y SEGURA):</strong> Reinstala los archivos del sistema operativo y repara la configuración de arranque corrupta. <strong>NO borra tus juegos de retail, ni tus partidas, ni tus aplicaciones o datos instalados en Dev Mode.</strong></li>
            <li><strong style="color: #D9381E;">"Restablecer y quitar todo" (NO SELECCIONAR):</strong> Borra absolutamente todo el contenido de la consola y la devuelve a estado de fábrica.</li>
        </ul>
    </li>
    <li>Selecciona <strong>"Restablecer y mantener mis juegos y aplicaciones"</strong> y confirma con <strong>[A]</strong>.</li>
    <li>La consola tardará unos 5 a 10 minutos en reinstalar el sistema operativo. Una vez finalizado, inicia sesión con tu cuenta de Microsoft y el error habrá desaparecido al 100%.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img12_solucion3_soft_reset.png" class="figure-img" alt="Opciones de restablecimiento de consola en Xbox">
    <div class="figure-caption">Figura 12: Selección de la opción segura 'Restablecer y mantener mis juegos y aplicaciones'.</div>
</div>

<hr>

<!-- CAPÍTULO 8: SOLUCIÓN N64 EN RETROARCH -->
<h2>8. Fase 6: Solución a Errores de Nintendo 64 en RetroArch ("Error en el contenido" y "Fallo en el núcleo")</h2>

<p>
Al cargar juegos de <strong>Nintendo 64</strong> en RetroArch para Xbox, es sumamente habitual encontrar los mensajes de error:
</p>
<center style="margin: 10px 0;">
    <span class="badge badge-error">Error en el contenido: Fallo en el núcleo al iniciarlo</span> &nbsp;&nbsp;
    <span class="badge badge-error">Failed to open libretro core</span>
</center>
<p>
Este fallo ocurre de forma idéntica tanto al seleccionar el núcleo <strong>Mupen64Plus-Next</strong> como el núcleo <strong>ParaLLEl N64</strong>. A continuación se desglosan las causas exactas en la plataforma UWP de Xbox y la guía paso a paso para resolverlo por completo.
</p>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img13_retroarch_n64_error.png" class="figure-img" alt="Pantalla de error al iniciar juegos de N64 en RetroArch Xbox">
    <div class="figure-caption">Figura 13: Notificación de fallo en el núcleo al cargar ROMs de Nintendo 64 en RetroArch Xbox.</div>
</div>

<h3>Diagnóstico Técnico: ¿Por qué fallan Mupen64Plus-Next y ParaLLEl N64 en Xbox?</h3>
<ol>
    <li><strong>Restricción de Recursos en Dev Home (Tipo "App"):</strong> Por defecto, cuando instalas RetroArch en Dev Mode, el sistema operativo le asigna la categoría de <em>App</em>. En este modo, Xbox restringe la aplicación a un solo núcleo de CPU y solo <strong>1 a 1,5 GB de RAM</strong>, además de capar el acceso directo al hardware gráfico. Los emuladores de sistemas 3D como Nintendo 64 colapsan al intentar reservar búferes de textura y memoria de vídeo si no están configurados en modo <em>Game</em>.</li>
    <li><strong>Incompatibilidad del Controlador de Vídeo Direct3D 12 / OpenGL:</strong> El plugin gráfico predeterminado de Mupen64Plus-Next es <strong>GLideN64</strong>. En Xbox, este plugin funciona a través de una capa de traducción OpenGL llamada ANGLE sobre Direct3D 11. Si el controlador de vídeo de RetroArch está ajustado en <code>d3d12</code> o <code>gl</code>, la capa ANGLE falla y el núcleo se cierra antes de mostrar imagen.</li>
    <li><strong>ParaLLEl N64 y la falta de Vulkan:</strong> El núcleo ParaLLEl N64 fue diseñado para renderizado de bajo nivel mediante la API Vulkan. <strong>Las consolas Xbox NO disponen de controladores Vulkan</strong>. Por tanto, intentar iniciar ParaLLEl N64 con sus plugins predeterminados (Parallel RDP/RSP) provoca un crash instantáneo en el 100% de los casos.</li>
    <li><strong>Compresión de ROMs (.zip / .7z):</strong> Descomprimir ROMs de Nintendo 64 (cuyo tamaño oscila entre 16 MB y 64 MB) en tiempo real en la memoria restringida de la partición UWP suele saturar el búfer de descompresión temporal.</li>
    <li><strong>Permisos de escritura en el Pendrive (<code>E:\</code>):</strong> Si la ROM se encuentra en un pendrive USB formateado en NTFS que no cuenta con los permisos de <code>ALL APPLICATION PACKAGES</code>, el emulador no puede crear los archivos de guardado (<code>.srm</code> o <code>.state</code>), provocando el bloqueo del contenido.</li>
</ol>

<hr>

<h3>Solución Paso a Paso: Protocolo de Configuración Óptima</h3>

<h4>Paso 1: Configurar RetroArch como "Game" en Dev Home (Paso Clave e Imprescindible)</h4>
<p>
Este es el cambio más importante y la causa del 90% de los cierres inesperados de núcleos 3D en Xbox:
</p>
<ol>
    <li>Sal de RetroArch y ve a la pantalla principal de <strong>Dev Home</strong>.</li>
    <li>En la lista de aplicaciones instaladas, coloca el cursor sobre el mosaico de <strong>RetroArch</strong>.</li>
    <li>Presiona el <strong>botón Vista</strong> (los dos rectángulos superpuestos) o el <strong>botón Menú</strong> (☰) en tu mando y selecciona la opción <strong>"View details"</strong> (Ver detalles).</li>
    <li>En la ventana de propiedades, localiza el campo <strong>"App type"</strong> (Tipo de aplicación).</li>
    <li>Cambia el valor de <strong>"App"</strong> a <strong>"Game"</strong> (Juego).</li>
    <li>Pulsa el botón <strong>Save</strong> (Guardar).</li>
    <li><strong style="color: #D9381E;">REINICIA LA CONSOLA:</strong> Para que el kernel de Xbox asigne la memoria ampliada (más de 5 GB de RAM y los 8 núcleos de CPU completos a RetroArch), debes reiniciar la consola desde el menú de Dev Home.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img14_app_type_game.png" class="figure-img" alt="Configuración de RetroArch como Game en Dev Home">
    <div class="figure-caption">Figura 14: Cambio de App Type a 'Game' en Dev Home para desbloquear la potencia total del hardware de Xbox.</div>
</div>

<hr>

<h4>Paso 2: Ajustar el Controlador de Vídeo a "d3d11" en RetroArch</h4>
<p>
Para que el emulador traduzca correctamente los gráficos de Nintendo 64 en Xbox:
</p>
<ol>
    <li>Abre <strong>RetroArch</strong>.</li>
    <li>En el menú principal, dirígete a <strong>Ajustes</strong> (icono de engranaje).</li>
    <li>Selecciona <strong>Controladores</strong> (Drivers).</li>
    <li>En la opción <strong>Vídeo</strong> (Video), pulsa [A] y selecciona estrictamente <code>d3d11</code>.</li>
    <li><strong style="color: #107C10;">Guardar la configuración:</strong> Regresa al <em>Menú principal ➔ Archivo de configuración ➔ Guardar configuración actual</em>.</li>
    <li>Cierra RetroArch completamente (<em>Menú principal ➔ Salir de RetroArch</em>) y vuelve a abrirlo para que el motor gráfico inicialice con el controlador <code>d3d11</code>.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img15_retroarch_video_driver.png" class="figure-img" alt="Configuración del controlador de vídeo a d3d11 en RetroArch">
    <div class="figure-caption">Figura 15: Configurar el controlador de vídeo en 'd3d11' para garantizar la compatibilidad con GLideN64.</div>
</div>

<div class="warning">
    <div class="warning-title">⚠️ ¡Atención con d3d12 y GLCore!</div>
    No selecciones <code>d3d12</code> para Nintendo 64 en consolas Xbox One o Series, ya que el plugin GLideN64 presente en las versiones UWP actuales provocará cierres forzados continuos. Mantén siempre <code>d3d11</code>.
</div>

<hr>

<h4>Paso 3: Selección de Núcleo y Configuración de Plugins Gráficos</h4>
<p>
No todos los núcleos de N64 se comportan de la misma forma en Xbox:
</p>

<ul>
    <li><strong style="color: #107C10;">Núcleo Recomendado: Mupen64Plus-Next</strong><br>
        Es el núcleo más compatible, rápido y estable en Xbox. Una vez que hayas aplicado el Paso 1 y Paso 2, abrirá tus ROMs con total normalidad.<br>
        • <em>Plugin gráfico (RDP):</em> <code>GLideN64</code> (óptimo para reescalar resolución a 1080p / 4K).<br>
        • <em>Plugin de audio/procesamiento (RSP):</em> <code>HLE</code> (High Level Emulation).
    </li>
    <li><strong style="color: #D9381E;">¿Por qué falla ParaLLEl N64 y cómo solucionarlo?</strong><br>
        Si deseas usar ParaLLEl N64, <strong>debes desactivar obligatoriamente el renderizado Vulkan</strong>. Para ello, entra al juego o edita su configuración para establecer:<br>
        • <em>GFX Plugin:</em> <code>angrylion</code> (renderizado por software en CPU, sumamente fiel al hardware original pero más exigente).<br>
        • <em>RSP Plugin:</em> <code>hle</code> o <code>cxd4</code>.<br>
        <em>Si ParaLLEl tiene asignado el plugin 'parallel-rdp', colapsará siempre debido a la ausencia de Vulkan en Xbox.</em>
    </li>
</ul>

<hr>

<h4>Paso 4: Descompresión de ROMs y Permisos en la Unidad USB <code>E:\</code></h4>
<ol>
    <li><strong>Descomprimir las ROMs:</strong> No ejecutes archivos en formato <code>.zip</code>, <code>.7z</code> ni <code>.rar</code>. Descomprime tus juegos en tu ordenador antes de copiarlos al pendrive. Las extensiones válidas de Nintendo 64 son:
        <ul>
            <li><code>.z64</code> (Formato estándar Big-Endian, el más recomendado y compatible).</li>
            <li><code>.n64</code> (Formato Little-Endian).</li>
            <li><code>.v64</code> (Formato Byte-swapped).</li>
        </ul>
    </li>
    <li><strong>Verificar permisos en el Pendrive (<code>E:\</code>):</strong> Asegúrate de que el pendrive tenga formato <strong>NTFS</strong> y permisos de <strong>ALL APPLICATION PACKAGES</strong> (Control Total), tal como se explicó en los requisitos de almacenamiento. De lo contrario, RetroArch no podrá escribir el archivo temporal de verificación de cabecera de la ROM.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img16_n64_core_and_roms.png" class="figure-img" alt="Configuración de núcleos de N64 y gestión de ROMs">
    <div class="figure-caption">Figura 16: Tabla de configuración de núcleos de Nintendo 64, plugins y formato de archivos desarchivados.</div>
</div>

<hr>

<h4>Paso 5: Archivo de Rescate de Configuración (<code>mupen64plus-next.opt</code>)</h4>
<p>
Si un juego de N64 provocó que el núcleo guardara una opción errónea y ahora RetroArch se cierra inmediatamente antes de que puedas entrar al <em>Menú Rápido</em> para cambiar el plugin, puedes forzar la configuración correcta mediante un archivo de texto:
</p>
<ol>
    <li>Conecta tu pendrive USB (<code>E:\</code>) a tu ordenador.</li>
    <li>Navega hasta la carpeta de configuraciones de RetroArch: <code>E:\RetroArch\config\Mupen64Plus-Next\</code> (si la carpeta no existe, puedes crearla).</li>
    <li>Crea o edita un archivo de texto llamado <code>mupen64plus-next.opt</code> con el Bloc de notas.</li>
    <li>Pega las siguientes líneas esenciales de rescate:
<pre style="background-color: #1E1E1E; color: #00FF66; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 9.5pt;">
mupen64plus-rdp-plugin = "gliden64"
mupen64plus-rsp-plugin = "hle"
mupen64plus-43screensize = "640x480"
mupen64plus-aspect = "4:3"
mupen64plus-screensize = "1280x960"
</pre>
    </li>
    <li>Guarda el archivo, conecta el pendrive a tu Xbox y vuelve a lanzar el juego. El núcleo arrancará forzando el plugin compatible.</li>
</ol>

<hr>

<h4>Paso 6: Actualización de Core Info Files y Prevención de Núcleos Rotos</h4>
<div class="callout">
    <div class="callout-title">⚠️ IMPORTANTE: No actualizar núcleos desde el "Actualizador en Línea"</div>
    Muchas versiones compiladas que se descargan automáticamente desde <em>Menú principal ➔ Actualizador en línea ➔ Descargador de núcleos</em> están pensadas para Windows de escritorio x64 genérico y <strong>carecen de los parches específicos para UWP de Xbox</strong>. Si actualizas un núcleo desde allí, es muy probable que se rompa.<br><br>
    • <strong>Lo que SÍ debes actualizar:</strong> Ve a <em>Menú principal ➔ Actualizador en línea</em> y selecciona <strong>"Actualizar archivos de información de núcleos"</strong> (Core Info Files) y <strong>"Actualizar bases de datos"</strong>. Esto permitirá que RetroArch reconozca las cabeceras de tus ROMs de N64 sin tocar las librerías binarias del núcleo.
</div>

<hr>

<!-- CAPÍTULO 9: GUÍA MAESTRA DE BIOS EN RETROARCH -->
<h2>9. Fase 7: Guía Maestra de Carga de BIOS en RetroArch (Pendrive USB vs Memoria Interna)</h2>

<p>
Una de las preguntas más comunes e importantes al configurar la emulación en Xbox Dev Mode es:  
<strong>¿Cómo se cargan las BIOS de las consolas y dónde es mejor colocarlas: en el pendrive USB o en la memoria interna de la consola?</strong>
</p>

<h3>¿Qué es una BIOS y qué consolas la necesitan obligatoriamente?</h3>
<p>
La <strong>BIOS</strong> (Basic Input/Output System) es el software del sistema operativo original de la consola física (por ejemplo, el chip interno de PlayStation, Sega Saturn o Dreamcast). Contiene las rutinas de arranque, decodificación de vídeo y librerías que los emuladores requieren para ejecutar los juegos con fidelidad.
</p>
<ul>
    <li><strong>Consolas que NO requieren BIOS:</strong> NES, Super Nintendo, Nintendo 64, Game Boy, Game Boy Color, Sega Genesis / Mega Drive (los núcleos emulan el hardware directamente por software).</li>
    <li><strong>Consolas que SÍ REQUIEREN BIOS OBLIGATORIA:</strong> Sony PlayStation 1 (PS1), PlayStation 2 (PS2), Sega CD / Mega CD, Sega Saturn, Sega Dreamcast, Arcade Neo-Geo (<code>neogeo.zip</code>), Panasonic 3DO y Arcade Naomi. Sin su correspondiente BIOS, el núcleo mostrará pantalla negra o fallará al iniciar.</li>
    <li><strong>Consolas que se benefician de BIOS opcional:</strong> Game Boy Advance (mejora compatibilidad y muestra la animación oficial de inicio).</li>
</ul>

<hr>

<h3>Análisis Técnico: ¿Pendrive USB (E:\) o Almacenamiento Interno (U:\)?</h3>
<p>
Existen dos ubicaciones posibles para alojar las BIOS en una Xbox en Modo Desarrollador:
</p>

<table>
    <tr>
        <th>Criterio Técnico</th>
        <th>Pendrive USB Externo (E:\) ★ RECOMENDADO</th>
        <th>Memoria Interna SSD (U:\ / LocalState)</th>
    </tr>
    <tr>
        <td><strong>Seguridad de los archivos</strong></td>
        <td><strong>100% Protegido:</strong> Nunca se borra si reinstalas la app o sales de Dev Mode.</td>
        <td><strong>Riesgo Alto:</strong> Se borra si desinstalas RetroArch o si marcas por error "Delete sideloaded".</td>
    </tr>
    <tr>
        <td><strong>Facilidad de gestión</strong></td>
        <td><strong>Inmediata:</strong> Conectas el pendrive a tu PC y copias carpetas enteras de golpe.</td>
        <td><strong>Muy lenta:</strong> Obliga a usar Xbox Device Portal por navegador (puerto 11443) subiendo archivo a archivo.</td>
    </tr>
    <tr>
        <td><strong>Espacio disponible</strong></td>
        <td>Ilimitado (depende de tu pendrive o disco externo: 64 GB, 256 GB, 1 TB...).</td>
        <td>Limitado por la partición de desarrollo asignada internamente.</td>
    </tr>
    <tr>
        <td><strong>Portabilidad</strong></td>
        <td>Llevas tu pendrive a cualquier consola Xbox o PC y todo funciona al instante.</td>
        <td>Queda encerrado dentro de una única consola.</td>
    </tr>
    <tr>
        <td><strong>Rendimiento de lectura</strong></td>
        <td>Instantáneo (las BIOS pesan solo entre 512 KB y 8 MB; USB 3.0 sobra).</td>
        <td>Instantáneo.</td>
    </tr>
</table>

<div class="callout">
    <div class="callout-title">🏆 Conclusión Contundente</div>
    <strong>ES INFINITAMENTE MEJOR CARGAR LAS BIOS EN EL PENDRIVE USB (UNIDAD E:\).</strong><br>
    Colocarlas en el almacenamiento interno solo añade frustración: la interfaz web de Xbox Device Portal se bloquea al transferir archivos grandes, las rutas internas son extremadamente complejas (<code>U:\\Users\\DefaultAccount\\AppData\\Local\\Packages\\...</code>) y corres el riesgo de perder semanas de configuración si la aplicación se actualiza o se restablece. En el pendrive, tus BIOS estarán seguras de por vida.
</div>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img17_bios_pendrive_vs_interno.png" class="figure-img" alt="Comparativa de BIOS: Pendrive USB vs Memoria Interna">
    <div class="figure-caption">Figura 17: Análisis comparativo entre la gestión de BIOS en Pendrive USB (E:\) y el almacenamiento interno.</div>
</div>

<hr>

<h3>Estructura de Carpetas Recomendada en el Pendrive (<code>E:\</code>)</h3>
<p>
Para que RetroArch mantenga una organización impecable y profesional, crea la siguiente jerarquía de carpetas en la raíz de tu pendrive USB desde tu ordenador:
</p>

<pre style="background-color: #1A1C23; color: #00FF66; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 9.5pt;">
E:\ (Tu Pendrive USB en NTFS)
 ├── RetroArch\
 │    ├── system\               &lt;--- [AQUÍ SE COLOCAN TODAS LAS BIOS]
 │    │    ├── scph5500.bin     (BIOS PS1 Japón)
 │    │    ├── scph5501.bin     (BIOS PS1 América / NTSC-U)
 │    │    ├── scph5502.bin     (BIOS PS1 Europa / PAL)
 │    │    ├── gba_bios.bin     (BIOS Game Boy Advance - 16.384 bytes)
 │    │    ├── gbc_bios.bin     (BIOS Game Boy Color - 2.048 bytes, opcional)
 │    │    ├── neogeo.zip       (BIOS Arcade NeoGeo en la raíz de system)
 │    │    ├── dc\              (Subcarpeta para Sega Dreamcast)
 │    │    │    └── dc_boot.bin
 │    │    └── pcsx2\           (Subcarpeta para PlayStation 2)
 │    │         └── bios\
 │    │              └── ps2-0230a-20080220.bin
 │    ├── saves\                (Partidas guardadas estándar)
 │    ├── states\               (Estados de guardado rápido)
 │    └── config\               (Perfiles de núcleos)
 └── ROMS\                      (Tus carpetas de juegos organizadas por consola)
</pre>

<hr>

<h3>Paso a Paso: Cómo Configurar RetroArch para Leer las BIOS desde el Pendrive</h3>

<ol>
    <li>Conecta tu pendrive USB con la carpeta <code>system</code> preparada a uno de los puertos USB de tu consola Xbox.</li>
    <li>Abre <strong>RetroArch</strong> en la consola.</li>
    <li>En el menú principal, desplázate hasta el icono de <strong>Ajustes</strong> (engranaje).</li>
    <li>Baja hasta la opción <strong>Directorios</strong> (Directory) y pulsa <strong>[A]</strong>.</li>
    <li>Selecciona la primera opción: <strong>Sistema/BIOS</strong> (System/BIOS).</li>
    <li>Navega por la lista de unidades de almacenamiento hasta encontrar la letra <strong><code>E:\</code></strong> (tu pendrive).</li>
    <li>Entra en <code>E:\ ➔ RetroArch ➔ system</code>.</li>
    <li>Una vez dentro de la carpeta <em>system</em>, pulsa en la primera opción de la lista: <strong>"&lt;Usar este directorio&gt;"</strong> (&lt;Use this directory&gt;).</li>
    <li><strong style="color: #107C10;">Paso obligatorio para guardar:</strong> Regresa al <em>Menú principal ➔ Archivo de configuración ➔ Guardar configuración actual</em>.</li>
</ol>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img18_configurar_directorio_bios.png" class="figure-img" alt="Configuración de directorios y comprobación de BIOS en RetroArch">
    <div class="figure-caption">Figura 18: Asignación de la ruta 'E:\RetroArch\system' y verificación de firmas en Información del Núcleo.</div>
</div>

<hr>

<h3>Comprobación de Estado: Menú de Información del Núcleo</h3>
<p>
¿Cómo saber si RetroArch ha detectado tu BIOS correctamente antes de lanzar un juego? RetroArch cuenta con una herramienta integrada de diagnóstico:
</p>
<ol>
    <li>En el <strong>Menú principal</strong>, selecciona <strong>Cargar núcleo</strong> (Load Core).</li>
    <li>Selecciona el núcleo que vas a usar (por ejemplo, <em>Sony - PlayStation (PCSX ReARMed)</em> o <em>Beetle PSX HW</em>).</li>
    <li>Una vez cargado el núcleo, vuelve al menú principal y selecciona <strong>Información</strong> (Information).</li>
    <li>Entra en <strong>Información del núcleo</strong> (Core Information).</li>
    <li>Baja por la pantalla hasta la sección <strong>"Firmware / BIOS"</strong>:
        <ul>
            <li>Si la BIOS está en su sitio, tiene el nombre exacto y la firma MD5 correcta, verás un texto en verde brillante: <strong style="color: #00FF66;">(!) Presente</strong>.</li>
            <li>Si falta la BIOS o el nombre tiene alguna letra incorrecta, verás un aviso en rojo: <strong style="color: #D9381E;">(X) Ausente / Missing</strong>.</li>
        </ul>
    </li>
</ol>

<hr>

<h3>Tabla Maestra de BIOS por Consola</h3>
<p>
A continuación se detalla la lista de nombres exactos requeridos por los núcleos principales. Recuerda que los nombres de archivo son <strong>estrictamente sensibles a mayúsculas y minúsculas</strong> (deben ir exactamente en minúsculas salvo que se indique lo contrario):
</p>

<table>
    <tr>
        <th>Consola</th>
        <th>Núcleo Recomendado</th>
        <th>Ubicación exacta y Nombre de archivo</th>
        <th>Región / Propósito</th>
    </tr>
    <tr>
        <td rowspan="3"><strong>PlayStation 1 (PS1)</strong></td>
        <td rowspan="3">PCSX ReARMed / Beetle PSX</td>
        <td><code>system/scph5501.bin</code></td>
        <td>América (NTSC-U) - Esencial</td>
    </tr>
    <tr>
        <td><code>system/scph5500.bin</code></td>
        <td>Japón (NTSC-J)</td>
    </tr>
    <tr>
        <td><code>system/scph5502.bin</code></td>
        <td>Europa (PAL)</td>
    </tr>
    <tr>
        <td><strong>PlayStation 2 (PS2)</strong></td>
        <td>PCSX2 / LRPS2</td>
        <td><code>system/pcsx2/bios/ps2-0230a-20080220.bin</code><br><em>(o cualquier .bin oficial de PS2 en esa carpeta)</em></td>
        <td>Bios oficial de PS2 (requiere subcarpeta pcsx2/bios)</td>
    </tr>
    <tr>
        <td><strong>Sega Dreamcast</strong></td>
        <td>Flycast</td>
        <td><code>system/dc/dc_boot.bin</code><br><code>system/dc/dc_flash.bin</code></td>
        <td>Bootloader y memoria flash de Dreamcast</td>
    </tr>
    <tr>
        <td rowspan="2"><strong>Sega Saturn</strong></td>
        <td rowspan="2">Beetle Saturn / Yabause</td>
        <td><code>system/saturn_bios.bin</code></td>
        <td>América / Europa</td>
    </tr>
    <tr>
        <td><code>system/sega_101.bin</code></td>
        <td>Japón</td>
    </tr>
    <tr>
        <td rowspan="3"><strong>Sega CD / Mega CD</strong></td>
        <td rowspan="3">Genesis Plus GX / Picodrive</td>
        <td><code>system/bios_CD_U.bin</code></td>
        <td>USA (Sega CD)</td>
    </tr>
    <tr>
        <td><code>system/bios_CD_E.bin</code></td>
        <td>Europa (Mega CD)</td>
    </tr>
    <tr>
        <td><code>system/bios_CD_J.bin</code></td>
        <td>Japón (Mega CD)</td>
    </tr>
    <tr>
        <td><strong>Arcade Neo-Geo</strong></td>
        <td>FB Neo / MAME</td>
        <td><code>system/neogeo.zip</code></td>
        <td>Archivo ZIP sin descomprimir en la raíz de system</td>
    </tr>
    <tr>
        <td><strong>Game Boy Advance</strong></td>
        <td>mGBA / VBA Next</td>
        <td><code>system/gba_bios.bin</code></td>
        <td>Exactamente 16.384 bytes (16 KB)</td>
    </tr>
    <tr>
        <td><strong>Game Boy Color</strong></td>
        <td>Gambatte / SameBoy</td>
        <td><code>system/gbc_bios.bin</code></td>
        <td>Opcional (exactamente 2.048 bytes = 2 KB)</td>
    </tr>
</table>

<hr>

<!-- CAPÍTULO 10: SOLUCIÓN GBA EN RETROARCH -->
<h2>10. Fase 8: Solución al Error de Game Boy Advance (GBA): "Error en el contenido / No se puede cargar"</h2>

<p>
Un problema desconcertante que experimentan muchos usuarios al emular <strong>Game Boy Advance (GBA)</strong> en Xbox Dev Mode es el mensaje de fallo:
</p>
<center style="margin: 10px 0;">
    <span class="badge badge-error">Error en el contenido: no se puede cargar</span> &nbsp;&nbsp;
    <span class="badge badge-error">Failed to load content</span>
</center>
<p>
Incluso habiendo configurado la ruta de la carpeta <code>system</code> en los Ajustes de Directorio de RetroArch y habiendo colocado el archivo de la BIOS, la ROM se niega a arrancar. A continuación se desglosan las causas reales de este fallo en Xbox UWP y el protocolo paso a paso para dejar tus juegos de GBA 100% operativos.
</p>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img19_gba_error_content.png" class="figure-img" alt="Error de contenido en Game Boy Advance en RetroArch Xbox">
    <div class="figure-caption">Figura 19: Notificación de 'Error en el contenido' al iniciar ROMs de Game Boy Advance en Xbox.</div>
</div>

<h3>Diagnóstico Técnico: ¿Por qué falla GBA si ya seleccionaste la ruta de la BIOS?</h3>
<ol>
    <li><strong>El archivo de BIOS es falso, está corrupto o tiene peso erróneo (Causa Principal):</strong> La BIOS oficial de Game Boy Advance tiene un tamaño matemático estricto e invariable: <strong>exactamente 16.384 bytes (16,0 KB)</strong>. En internet circulan miles de descargas erróneas: volcados de 32 KB con cabeceras de emulador antiguo, archivos de 0 bytes o incluso páginas web HTML renombradas a <code>.bin</code>. Si el núcleo detecta una BIOS cuyo tamaño no son exactamente 16.384 bytes, aborta inmediatamente el inicio para proteger la memoria.</li>
    <li><strong>Sensibilidad a Mayúsculas y Nombre Erróneo:</strong> El archivo debe llamarse con estricta precisión: <code>gba_bios.bin</code> (en minúsculas). Si se llama <code>GBA.BIN</code>, <code>GBA_BIOS.BIN</code>, <code>bios_gba.bin</code> o <code>gba.bin</code>, RetroArch no lo asociará al núcleo.</li>
    <li><strong>Conflicto con el núcleo "gpSP" y su Dynarec en Xbox:</strong> Si estás intentando cargar el juego con el núcleo <em>Game Boy Advance (gpSP)</em>, este núcleo utiliza un recompilador dinámico de código (*Dynarec*). El entorno UWP seguro de Xbox bloquea la ejecución de código dinámico en ciertas páginas de memoria, provocando que gpSP crashee de inmediato.</li>
    <li><strong>ROMs comprimidas en .zip o .7z con archivos sobrantes:</strong> Los paquetes de ROMs de GBA a menudo se descargan en formato <code>.zip</code> conteniendo archivos <code>.txt</code> de información, carátulas o nombres con caracteres especiales (por ejemplo: <code>Pokemon - Esmeralda [!].zip</code>). RetroArch en Xbox falla al intentar desempaquetar estos archivos en el búfer temporal.</li>
    <li><strong>Permisos bloqueados al crear el archivo de guardado (.srm):</strong> Nada más abrir una ROM de GBA, el emulador inicializa en segundo plano el chip de memoria del cartucho creando un archivo <code>.srm</code> o <code>.sav</code> en la carpeta de guardados o junto a la ROM. Si tu pendrive <code>E:\</code> no tiene asignados los permisos NTFS de <code>ALL APPLICATION PACKAGES</code> con "Control Total", la función de escritura del sistema de archivos de Xbox devuelve *Access Denied* y el juego se detiene con error de contenido.</li>
</ol>

<hr>

<h3>Protocolo de Solución Rápida en 4 Pasos</h3>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img20_gba_solucion_paso_a_paso.png" class="figure-img" alt="Solución paso a paso para Game Boy Advance en RetroArch Xbox">
    <div class="figure-caption">Figura 20: Verificación de BIOS de 16 KB, asignación del núcleo mGBA y descompresión de ROMs.</div>
</div>

<h4>Paso 1: Verificar el archivo oficial de la BIOS de GBA</h4>
<p>
Conecta tu pendrive USB (<code>E:\</code>) a tu ordenador y verifica los datos de tu BIOS:
</p>
<ul>
    <li><strong>Ruta exacta en el Pendrive:</strong> <code>E:\RetroArch\system\gba_bios.bin</code></li>
    <li><strong>Nombre de archivo:</strong> <code>gba_bios.bin</code> (todo en minúsculas).</li>
    <li><strong>Tamaño en disco (Propiedades en Windows):</strong> Debe indicar exactamente <strong>16,0 KB (16.384 bytes)</strong>. Si indica 32 KB o un tamaño distinto, esa BIOS no sirve y debes reemplazarla.</li>
    <li><strong>Firma Hash MD5 oficial:</strong> <code>a860e8c0b6d573d191e4ec7db1b1e4f6</code>.</li>
</ul>

<h4>Paso 2: Cambiar al núcleo "mGBA" (o usar la BIOS interna HLE)</h4>
<p>
El núcleo <strong>mGBA</strong> es el estándar dorado de compatibilidad y estabilidad en consolas Xbox One y Xbox Series X|S:
</p>
<ol>
    <li>En RetroArch, ve a <strong>Cargar contenido</strong> ➔ Navega hasta tu juego de GBA en <code>E:\ROMS\GBA\</code>.</li>
    <li>Selecciona la opción <strong>"Cargar con el núcleo"</strong>.</li>
    <li>Elige expresamente <strong>Nintendo - Game Boy Advance (mGBA)</strong> (no utilices <em>gpSP</em>).</li>
    <li><strong>El truco de la BIOS interna de mGBA:</strong> Una de las mayores virtudes de mGBA es que cuenta con una BIOS virtual por software (HLE) integrada al 100%. Esto significa que <strong>mGBA NO NECESITA NINGUNA BIOS EXTERNA PARA FUNCIONAR</strong>. Si sospechas que tu archivo <code>gba_bios.bin</code> sigue dando problemas, simplemente renómbralo o quítalo temporalmente de la carpeta <code>system</code>; mGBA arrancará el 100% de los juegos de GBA de forma directa y limpia con su BIOS interna.</li>
    <li><em>Alternativa secundaria:</em> Si algún título específico diera tirones en una Xbox One original, puedes utilizar el núcleo alternativo <strong>Nintendo - Game Boy Advance (VBA Next)</strong>, que está sumamente optimizado para la arquitectura de Xbox.</li>
</ol>

<h4>Paso 3: Descomprimir la ROM a formato limpio ".gba"</h4>
<ul>
    <li>En tu ordenador, haz clic derecho sobre tu archivo <code>.zip</code> o <code>.7z</code> y descomprímelo.</li>
    <li>Asegúrate de que el archivo final tenga la extensión <strong><code>.gba</code></strong> (por ejemplo: <code>The Legend of Zelda - The Minish Cap.gba</code>).</li>
    <li>Renombra el archivo si tiene corchetes o símbolos raros como <code>[!]</code> o <code>(U) [b1]</code> para dejar un nombre limpio.</li>
    <li>Copia el archivo <code>.gba</code> a tu pendrive <code>E:\ROMS\GBA\</code>.</li>
</ul>

<h4>Paso 4: Comprobar los permisos NTFS de guardado</h4>
<p>
Para evitar que el emulador colapse al intentar generar el archivo de guardado <code>.srm</code>:
</p>
<ol>
    <li>En tu ordenador con Windows, haz clic derecho sobre la unidad de tu pendrive <code>E:\</code> y selecciona <strong>Propiedades</strong>.</li>
    <li>Entra en la pestaña <strong>Seguridad</strong> ➔ haz clic en <strong>Opciones avanzadas</strong>.</li>
    <li>Asegúrate de que esté agregado el grupo <strong><code>ALL APPLICATION PACKAGES</code></strong> con permisos de <strong>Control Total</strong>.</li>
    <li>Marca la casilla inferior: <strong>"Reemplazar todas las entradas de permisos de objetos secundarios por permisos heredables de este objeto"</strong> y pulsa <strong>Aplicar</strong>. Esto otorgará permisos de escritura a todas tus carpetas de ROMs y a la carpeta <code>RetroArch\saves\</code>.</li>
</ol>

<hr>

<!-- CAPÍTULO 11: SOLUCIÓN GBC (WARIO LAND 3) EN RETROARCH -->
<h2>11. Fase 9: Solución al Error de Game Boy Color (GBC): Caso Real "Wario Land 3" y Fallos de Carga</h2>

<p>
Al intentar ejecutar juegos de <strong>Game Boy Color (GBC)</strong>, y muy señaladamente títulos complejos como <strong>Wario Land 3</strong>, es habitual encontrarse con el mismo bloqueo:
</p>
<center style="margin: 10px 0;">
    <span class="badge badge-error">Error en el contenido: no se puede cargar</span> &nbsp;&nbsp;
    <span class="badge badge-error">Failed to load content</span>
</center>
<p>
El caso de <em>Wario Land 3</em> es emblemático porque es uno de los juegos técnicamente más avanzados de Game Boy Color. A continuación se desglosan las causas que provocan su fallo y la solución definitiva para jugar sin interrupciones.
</p>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img21_gbc_error_wario.png" class="figure-img" alt="Error de contenido en Wario Land 3 para Game Boy Color en Xbox">
    <div class="figure-caption">Figura 21: Diagnóstico de fallo de inicio con la ROM de Wario Land 3 en Game Boy Color.</div>
</div>

<h3>Diagnóstico Técnico: ¿Por qué falla Wario Land 3 en RetroArch Xbox?</h3>
<ol>
    <li><strong>Asociación Errónea con Núcleos Exclusivos de GBA (Causa más habitual):</strong> Si anteriormente configuraste núcleos como <em>gpSP</em> o <em>VBA-M</em> para Game Boy Advance, o si creaste una lista de reproducción automática, RetroArch puede intentar abrir <em>Wario Land 3</em> con un núcleo exclusivo de GBA de 32 bits. Los núcleos puros de GBA no entienden las instrucciones de la CPU Z80 de 8 bits de Game Boy Color y abortan al instante.</li>
    <li><strong>La Arquitectura Especial de Wario Land 3 (Chip MBC3 + RTC + SRAM):</strong> A diferencia de juegos sencillos de plataformas, el cartucho físico de <em>Wario Land 3</em> incluía un coprocesador <strong>MBC3 con Reloj en Tiempo Real (RTC)</strong> para gestionar el paso del día y la noche en el mundo del juego, además de memoria SRAM con batería. Nada más pulsar en iniciar, el emulador necesita crear simultáneamente dos archivos en disco:
        <ul>
            <li><code>Wario Land 3.srm</code> (Memoria de guardado de partidas).</li>
            <li><code>Wario Land 3.rtc</code> (Estado del reloj de eventos temporales).</li>
        </ul>
        Si el pendrive USB <code>E:\</code> no cuenta con permisos de escritura completos, el emulador recibe una excepción de acceso de Windows UWP y arroja <em>"Error en el contenido"</em> antes de mostrar la pantalla de título.</li>
    <li><strong>El mito de la BIOS de GBC (gbc_bios.bin):</strong> Muchos usuarios descargan BIOS de internet creyendo que son obligatorias. <strong>Para Game Boy Color NO SE NECESITA NINGUNA BIOS EXTERNA</strong>. Núcleos oficiales como <em>Gambatte</em> emulan el arranque a la perfección por software (HLE). Si colocas en tu carpeta <code>system</code> un archivo llamado <code>gbc_bios.bin</code> que esté corrupto o que no pese exactamente <strong>2.048 bytes (2,0 KB)</strong>, el núcleo intentará forzar su lectura y colapsará.</li>
    <li><strong>ROM comprimida en .zip o con cabecera alterada:</strong> En muchas colecciones de internet, <em>Wario Land 3</em> viene empaquetado como <code>Wario Land 3 (World) (En,Ja) [!].zip</code>. El descompresor interno de RetroArch UWP a menudo se bloquea con caracteres especiales o extensiones anidadas.</li>
</ol>

<hr>

<h3>Protocolo de Solución Definitiva para Wario Land 3 y Game Boy Color</h3>

<div class="figure-container">
    <img src="{ASSETS_DIR}/img22_gbc_solucion_gambatte.png" class="figure-img" alt="Solución definitiva para Game Boy Color con Gambatte">
    <div class="figure-caption">Figura 22: Protocolo con núcleo Gambatte, extracción .gbc y gestión de guardados RTC (.srm / .rtc).</div>
</div>

<h4>Paso 1: Asignar el núcleo oficial correcto: "Gambatte"</h4>
<p>
El núcleo oficial y definitivo para Game Boy y Game Boy Color en Xbox es <strong>Gambatte</strong>:
</p>
<ol>
    <li>En RetroArch, ve a <strong>Menú principal</strong> ➔ <strong>Cargar contenido</strong>.</li>
    <li>Navega por tu pendrive hasta la carpeta de tus juegos de GBC: <code>E:\ROMS\GBC\</code>.</li>
    <li>Selecciona tu archivo de <strong>Wario Land 3.gbc</strong>.</li>
    <li>Pulsa en la opción <strong>"Cargar con el núcleo"</strong>.</li>
    <li>En la lista de núcleos disponibles, selecciona expresamente:  
        <strong style="color: #00FF66;">Nintendo - Game Boy / Color (Gambatte)</strong>.</li>
    <li><em>(Alternativa secundaria muy buena: <strong>Nintendo - Game Boy / Color (SameBoy)</strong> o <strong>Gearboy</strong>).</em></li>
</ol>

<h4>Paso 2: Descomprimir la ROM a formato limpio ".gbc"</h4>
<p>
No cargues nunca <em>Wario Land 3</em> dentro de un archivo <code>.zip</code> o <code>.7z</code>:
</p>
<ul>
    <li>En tu PC, abre el archivo comprimido y extrae la ROM.</li>
    <li>Renómbrala para dejar un nombre corto y limpio, sin paréntesis ni corchetes: <code>Wario Land 3.gbc</code>.</li>
    <li>Verifica su tamaño en las propiedades de Windows: debe pesar exactamente <strong>2.097.152 bytes (2,0 MB)</strong>.</li>
    <li>Copia el archivo resultante a tu carpeta <code>E:\ROMS\GBC\</code>.</li>
</ul>

<h4>Paso 3: Eliminar o corregir la BIOS de GBC</h4>
<p>
Para evitar que Gambatte colapse buscando una BIOS defectuosa:
</p>
<ul>
    <li>Entra a la carpeta <code>E:\RetroArch\system\</code> en tu pendrive.</li>
    <li>Si tienes un archivo llamado <code>gbc_bios.bin</code>, comprueba sus propiedades: si no pesa exactamente <strong>2.048 bytes (2 KB)</strong>, <strong>ELIMÍNALO</strong> o muévelo fuera.</li>
    <li>Sin ese archivo, <em>Gambatte</em> utilizará automáticamente su BIOS por software de alto nivel (HLE), que es 100% compatible y reproduce la animación oficial de inicio de Game Boy Color con la paleta de colores original de Nintendo.</li>
</ul>

<h4>Paso 4: Otorgar permisos de escritura en la carpeta de GBC (Creación de .srm y .rtc)</h4>
<p>
Como <em>Wario Land 3</em> genera los archivos de guardado <code>.srm</code> y de reloj <code>.rtc</code>:
</p>
<ol>
    <li>Conecta tu pendrive USB al PC.</li>
    <li>Haz clic derecho sobre la carpeta <code>E:\ROMS\GBC\</code> (o sobre la raíz del pendrive <code>E:\</code>) ➔ <strong>Propiedades</strong>.</li>
    <li>Pestaña <strong>Seguridad</strong> ➔ <strong>Opciones avanzadas</strong>.</li>
    <li>Verifica que el usuario <strong><code>ALL APPLICATION PACKAGES</code></strong> esté presente y tenga marcado <strong>Control Total</strong>.</li>
    <li>Haz clic en <strong>"Reemplazar todas las entradas de permisos de objetos secundarios por permisos heredables de este objeto"</strong> y pulsa en <strong>Aceptar</strong>.</li>
</ol>
<p>
Tras aplicar estos pasos, conecta el pendrive a tu Xbox, selecciona la ROM con el núcleo <strong>Gambatte</strong> y <em>Wario Land 3</em> arrancará de forma inmediata, fluida y con guardado de partidas plenamente funcional.
</p>

<hr>

<!-- CAPÍTULO 12 -->
<h2>12. Fase 10: Otras Preguntas Frecuentes y Solución de Problemas Generales</h2>

<h3>¿Qué hago si la app da error "Access Denied" (Acceso Denegado)?</h3>
<p>
Este error ocurre cuando la cuenta de Microsoft utilizada en la consola no tiene completado el perfil de desarrollador en Partner Center o no se ha confirmado el pago de registro.
</p>
<ul>
    <li>Inicia sesión en <a href="https://partner.microsoft.com">partner.microsoft.com</a> desde tu PC y comprueba que tu estado de cuenta muestre "Active" (Activo).</li>
    <li><strong>Método alternativo (Menú secreto de desarrollador):</strong> En la consola, ve a <em>Configuración ➔ Sistema ➔ Información de la consola</em>. En esa pantalla, presiona en tu mando la siguiente combinación de gatillos y botones superiores simultáneamente: <code>LB + RB + LT + RT</code>. Se abrirá una pestaña oculta llamada <em>"Developer Settings"</em> donde puedes forzar la activación.</li>
</ul>

<h3>¿Por qué no puedo jugar a mis juegos de disco o digitales en Dev Mode?</h3>
<p>
Por diseño estricto de seguridad de Microsoft, el Modo Desarrollador desactiva los certificados de cifrado antipiratería de los juegos comerciales. Para jugar a cualquier juego de tienda o Game Pass, debes volver a Modo Retail mediante el procedimiento explicado en la Fase 3.
</p>

<h3>¿Puedo perder mis juegos de Retail o partidas al usar Dev Mode?</h3>
<p>
No. Las particiones del disco duro están estrictamente separadas por la máquina virtual Hyper-V de la consola. Tus partidas guardadas en Retail se sincronizan además con la nube de Xbox Network, por lo que nunca se ven afectadas por nada de lo que ocurra en Dev Mode.
</p>

<h3>¿Cómo desactivo el Modo Desarrollador de forma definitiva?</h3>
<p>
Si vas a vender tu consola o deseas eliminar por completo el registro de desarrollo:
</p>
<ol>
    <li>En la consola, abre la app <em>Xbox Dev Mode</em> y selecciona la opción <strong>"Deactivate"</strong> (Desactivar).</li>
    <li>En tu PC, ingresa a <a href="https://partner.microsoft.com/xboxconfig/devices">partner.microsoft.com/xboxconfig/devices</a> y elimina la consola de tu lista de dispositivos (cada cuenta permite hasta 3 consolas simultáneas).</li>
    <li>Desinstala la app <em>Xbox Dev Mode</em> de la consola.</li>
</ol>

<hr>

<!-- CAPÍTULO 13 -->
<h2>13. Fase 11: Tabla Comparativa y Resumen de Accesos</h2>

<table>
    <tr>
        <th>Característica</th>
        <th>Modo Retail</th>
        <th>Modo Desarrollador (Dev)</th>
    </tr>
    <tr>
        <td><strong>Juegos comerciales / Game Pass</strong></td>
        <td>✓ Totalmente funcional</td>
        <td>✗ Deshabilitado</td>
    </tr>
    <tr>
        <td><strong>Multijugador Xbox Network / Logros</strong></td>
        <td>✓ Oficial y activo</td>
        <td>✗ No disponible</td>
    </tr>
    <tr>
        <td><strong>Emuladores y Homebrew (UWP)</strong></td>
        <td>✗ Bloqueado</td>
        <td>✓ Totalmente funcional</td>
    </tr>
    <tr>
        <td><strong>Xbox Device Portal (Gestión por PC)</strong></td>
        <td>✗ Inactivo</td>
        <td>✓ Activo en puerto 11443</td>
    </tr>
    <tr>
        <td><strong>Riesgo para la consola</strong></td>
        <td>0% (Modo estándar)</td>
        <td>0% (Sandbox oficial)</td>
    </tr>
    <tr>
        <td><strong>Garantía de Microsoft</strong></td>
        <td>Intacta</td>
        <td>Intacta</td>
    </tr>
</table>

<div class="tip">
    <div class="tip-title">💡 Resumen Clave de Configuración Óptima</div>
    Para disfrutar de una experiencia de emulación perfecta en Xbox Dev Mode:
    <ol>
        <li>Configura RetroArch como <strong>Game</strong> en Dev Home (no como <em>App</em>).</li>
        <li>Mantén el controlador de vídeo de RetroArch en <strong>d3d11</strong>.</li>
        <li>Utiliza un pendrive USB formateado en <strong>NTFS</strong> con permisos de <strong>ALL APPLICATION PACKAGES</strong> (unidad <code>E:\</code>).</li>
        <li>Carga todas las BIOS en la carpeta <strong><code>E:\RetroArch\system\</code></strong> y vincula esa ruta en <em>Ajustes ➔ Directorios</em>.</li>
        <li>Para <strong>Nintendo 64</strong>, utiliza el núcleo <strong>Mupen64Plus-Next</strong> con ROMs en <code>.z64</code>.</li>
        <li>Para <strong>Game Boy Advance</strong>, utiliza el núcleo <strong>mGBA</strong> con ROMs descomprimidas en <code>.gba</code>.</li>
        <li>Para <strong>Game Boy Color</strong> (ej. <em>Wario Land 3</em>), utiliza el núcleo <strong>Gambatte</strong> con ROMs descomprimidas en <code>.gbc</code> y asegúrate de permitir la creación de archivos <code>.srm</code> y <code>.rtc</code>.</li>
    </ol>
</div>

<p style="text-align: center; color: #777777; margin-top: 40px; font-size: 10pt;">
— Fin del Manual —<br>
<em>Documento generado en formato estándar OpenDocument Text (.odt) para libre distribución y consulta técnica.</em>
</p>

</body>
</html>
"""

def generate_odt():
    print("Writing HTML file...")
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print("Converting HTML to ODT with LibreOffice...")
    cmd = f"libreoffice --headless --convert-to odt {HTML_PATH} --outdir /tmp"
    ret = os.system(cmd)
    if ret != 0:
        print("Error converting with LibreOffice", file=sys.stderr)
        sys.exit(1)
        
    generated_raw = "/tmp/manual_xbox.odt"
    if not os.path.exists(generated_raw):
        print("Raw ODT was not generated!", file=sys.stderr)
        sys.exit(1)

    print("Embedding all images into ODT package...")
    extract_dir = "/tmp/manual_xbox_extracted"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    with zipfile.ZipFile(generated_raw, "r") as z:
        z.extractall(extract_dir)

    pics_dir = os.path.join(extract_dir, "Pictures")
    os.makedirs(pics_dir, exist_ok=True)

    content_xml_path = os.path.join(extract_dir, "content.xml")
    with open(content_xml_path, "r", encoding="utf-8") as f:
        xml_str = f.read()

    manifest_path = os.path.join(extract_dir, "META-INF", "manifest.xml")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_str = f.read()

    def replace_img_ref(match):
        full = match.group(0)
        href = match.group(1)
        if href.startswith("Pictures/"):
            return full
        base_name = os.path.basename(href)
        dest_path = os.path.join(pics_dir, base_name)
        src_candidates = [
            os.path.normpath(os.path.join("/tmp", href)),
            os.path.join(ASSETS_DIR, base_name),
            href
        ]
        found_src = None
        for cand in src_candidates:
            if os.path.exists(cand):
                found_src = cand
                break
        
        if found_src:
            shutil.copyfile(found_src, dest_path)
            print(f"Embedded: {base_name} ({os.path.getsize(dest_path)} bytes)")
            return f'xlink:href="Pictures/{base_name}"'
        else:
            print(f"Warning: image not found for {href}")
            return full

    new_xml = re.sub(r'xlink:href="([^"]+\.(?:png|jpg|jpeg|gif|webp))"', replace_img_ref, xml_str)
    with open(content_xml_path, "w", encoding="utf-8") as f:
        f.write(new_xml)

    # Update manifest.xml
    manifest_entries = ""
    for p in os.listdir(pics_dir):
        mime = "image/png" if p.endswith(".png") else "image/jpeg"
        entry = f'<manifest:file-entry manifest:full-path="Pictures/{p}" manifest:media-type="{mime}"/>'
        if entry not in manifest_str:
            manifest_entries += f"\n  {entry}"

    if manifest_entries:
        manifest_str = manifest_str.replace("</manifest:manifest>", f"{manifest_entries}\n</manifest:manifest>")
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_str)

    # Re-pack final ODT
    print("Packaging final ODT document...")
    with zipfile.ZipFile(FINAL_ODT, "w", zipfile.ZIP_DEFLATED) as z:
        mimetype_file = os.path.join(extract_dir, "mimetype")
        if os.path.exists(mimetype_file):
            z.write(mimetype_file, "mimetype", compress_type=zipfile.ZIP_STORED)
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file == "mimetype" and root == extract_dir:
                    continue
                fpath = os.path.join(root, file)
                arcname = os.path.relpath(fpath, extract_dir)
                z.write(fpath, arcname)

    print(f"Success! Final ODT saved to {FINAL_ODT}")
    print(f"Size: {os.path.getsize(FINAL_ODT)} bytes")

if __name__ == "__main__":
    generate_odt()
