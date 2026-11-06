#!/usr/bin/env bash
# ==============================================================================
# Script de Reparación y Recompilación Oficial de Engrampa para Ubuntu/Debian
# ==============================================================================
# Soluciona:
# 1. Violación de segmento (SIGSEGV) al abrir archivos RAR 7.x con directorios
# 2. Advertencias GLib-CRITICAL "g_strchomp: assertion 'string != NULL' failed"
# 3. Soporte para contraseña en RAR 7.x
# 4. Errores críticos al procesar fechas inválidas en propiedades/listados
# 5. Vulnerabilidad de Path Traversal en extracción de RPM (CVE-2023-52138)
# 6. Fallos de parseo en archivos LHA
# 7. Fugas de memoria detectadas por upstream
#
# Uso:
#   sudo bash reparar_engrampa_root.sh
# ==============================================================================

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "[-] Error: Este script debe ejecutarse como root (con sudo)."
    echo "    Ejemplo: sudo bash $0"
    exit 1
fi

REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)

echo "=========================================================="
echo " [Engrampa] Reparación del Sistema y Recompilación Oficial"
echo "=========================================================="
echo "Usuario detectado: $REAL_USER"
echo "Directorio personal: $REAL_HOME"

echo ""
echo "[1/6] Actualizando lista de paquetes e instalando dependencias de compilación..."
apt-get update
apt-get install -y --no-install-recommends \
    devscripts dpkg-dev debhelper build-essential \
    libgtk-3-dev libmagic-dev libjson-glib-dev libcaja-extension-dev \
    mate-common intltool yelp-tools \
    unar p7zip-full arj lhasa

echo ""
echo "[2/6] Creando entorno de trabajo temporal..."
WORK_DIR=$(mktemp -d -t engrampa-build-XXXXXX)
cd "$WORK_DIR"
chown "$REAL_USER:$REAL_USER" "$WORK_DIR"

echo ""
echo "[3/6] Obteniendo el código fuente oficial de engrampa..."
sudo -u "$REAL_USER" apt-get source engrampa

SRC_DIR=$(find . -maxdepth 1 -type d -name "engrampa-*" | head -n 1)
if [ -z "$SRC_DIR" ]; then
    echo "[-] Error: No se pudo descargar el código fuente de engrampa."
    rm -rf "$WORK_DIR"
    exit 1
fi

echo ""
echo "[4/6] Integrando parches upstream de corrección (RAR7, GLib, CVEs, etc.)..."
cd "$SRC_DIR"

mkdir -p debian/patches
PATCH_DEST="debian/patches/1002_upstream_fixes_rar7_and_security.patch"

cat << 'EOF' > "$PATCH_DEST"
diff --git a/src/dlg-open-with.c b/src/dlg-open-with.c
index 0f22c47..11a8c20 100644
--- a/src/dlg-open-with.c
+++ b/src/dlg-open-with.c
@@ -82,6 +82,7 @@ dlg_open_with (FrWindow *window,
 	app_chooser = gtk_app_chooser_dialog_new (GTK_WINDOW (window),
 						  GTK_DIALOG_MODAL,
 						  first_file);
+	g_object_unref (first_file);
 	g_signal_connect (app_chooser,
 			  "response",
 			  G_CALLBACK (app_chooser_response_cb),
diff --git a/src/dlg-package-installer.c b/src/dlg-package-installer.c
index d278987..81b55cd 100644
--- a/src/dlg-package-installer.c
+++ b/src/dlg-package-installer.c
@@ -214,6 +214,7 @@ install_packages (InstallerData *idata)
 					   _("There was an internal error trying to search for applications:"),
 					   error->message);
 		package_installer_terminated (idata, FR_PROC_ERROR_GENERIC, message);
+		g_free (message);
 
 		g_clear_error (&error);
 	}
diff --git a/src/dlg-prop.c b/src/dlg-prop.c
index cb8ed87..e82d5f1 100644
--- a/src/dlg-prop.c
+++ b/src/dlg-prop.c
@@ -101,10 +101,12 @@ dlg_prop (FrWindow *window)
 
 	GDateTime *date_time;
 	date_time = g_date_time_new_from_unix_local (get_file_mtime (fr_window_get_archive_uri (window)));
-	s = g_date_time_format (date_time, _("%d %B %Y, %H:%M"));
-	g_date_time_unref (date_time);
-	gtk_label_set_text (GET_LABEL ("p_date_label"), s);
-	g_free (s);
+	if (date_time) {
+		s = g_date_time_format (date_time, _("%d %B %Y, %H:%M"));
+		g_date_time_unref (date_time);
+		gtk_label_set_text (GET_LABEL ("p_date_label"), s);
+		g_free (s);
+	}
 
 	/**/
 
diff --git a/src/file-utils.c b/src/file-utils.c
index 44fed53..a5fbc68 100644
--- a/src/file-utils.c
+++ b/src/file-utils.c
@@ -144,6 +144,7 @@ get_dir_content_if_unique (const char  *uri)
 	if (err != NULL) {
 		g_warning ("Failed to enumerate children of %s: %s", uri, err->message);
 		g_error_free (err);
+		g_object_unref (file);
 		return NULL;
 	}
 
@@ -791,6 +792,8 @@ get_temp_work_dir (const char *parent_folder)
 		result = NULL;
 	}
 
+	g_free (best_folder);
+
 	return result;
 }
 
diff --git a/src/fr-command-lha.c b/src/fr-command-lha.c
index 22fd61d..5371f91 100644
--- a/src/fr-command-lha.c
+++ b/src/fr-command-lha.c
@@ -36,6 +36,18 @@ static void fr_command_lha_class_init  (FrCommandLhaClass *class);
 static void fr_command_lha_init        (FrCommand         *afile);
 static void fr_command_lha_finalize    (GObject           *object);
 
+enum {
+	FIELD_OS_OR_PERM,
+	FIELD_UID_GID,
+	FIELD_SIZE,
+	FIELD_RATIO,
+	FIELD_MONTH,
+	FIELD_DAY,
+	FIELD_TIME_OR_YEAR,
+	FIELD_FILENAME,
+	N_FIELDS
+};
+
 /* Parent Class */
 
 static FrCommandClass *parent_class = NULL;
@@ -96,75 +108,56 @@ static char **
 split_line_lha (char *line)
 {
 	char       **fields;
-	int          n_fields = 7;
-	const char  *scan;
+	const char  *scan, *field_end;
 	int          i;
 
-	fields = g_new0 (char *, n_fields + 1);
-	fields[n_fields] = NULL;
+	fields = g_new0 (char *, N_FIELDS + 1);
+	fields[N_FIELDS] = NULL;
 
 	i = 0;
 
-	if (strncmp (line, "[MS-DOS]", 8) == 0) {
-		fields[i++] = g_strdup ("");
-		fields[i++] = g_strdup ("");
-		line += strlen ("[MS-DOS]");
-	}
-	else if (strncmp (line, "[generic]", 9) == 0) {
-		fields[i++] = g_strdup ("");
-		fields[i++] = g_strdup ("");
-		line += strlen ("[generic]");
-	}
-	else if (strncmp (line, "[unknown]", 9) == 0) {
-		fields[i++] = g_strdup ("");
-		fields[i++] = g_strdup ("");
-		line += strlen ("[unknown]");
-	}
-	else if (strncmp (line, "[Amiga]", 7) == 0) {
-		fields[i++] = g_strdup ("");
-		fields[i++] = g_strdup ("");
-		line += strlen ("[Amiga]");
-	}
-
+	/* First column either contains Unix permissions or OS type, depending
+	 * on what generated the archive. The OS type is enclosed in [brackets]
+	 * and may include a space. */
 	scan = eat_spaces (line);
-	for (; i < n_fields; i++) {
-		const char *field_end;
-
-		if (NULL != (field_end = strchr (scan, ' '))) {
-			fields[i] = g_strndup (scan, field_end - scan);
-			scan = eat_spaces (field_end);
+	if (scan[0] == '[') {
+		field_end = strchr (scan, ']');
+		if (field_end != NULL) {
+			++field_end;
 		}
+	} else {
+		field_end = NULL;
 	}
 
-	return fields;
-}
-
-static const char *
-get_last_field_lha (char *line)
-{
-	int         i;
-	const char *field;
-	int         n = 7;
-
-	if (strncmp (line, "[MS-DOS]", 8) == 0)
-		n--;
+	if (field_end == NULL) {
+		field_end = strchr (scan, ' ');
+		if (field_end == NULL) {
+			field_end = scan + strlen(scan);
+		}
+	}
 
-	if (strncmp (line, "[generic]", 9) == 0)
-		n--;
+	fields[i++] = g_strndup (scan, field_end - scan);
+	scan = field_end;
 
-	if (strncmp (line, "[unknown]", 9) == 0)
-		n--;
+	/* Second column contains Unix UID/GID, but if the archive was not
+	 * made on a Unix system it will be empty. Insert a dummy value so
+	 * we get a consistent result. */
+	if (g_str_has_prefix (scan, "           ")) {
+		fields[i++] = g_strdup("");
+	}
 
-	if (strncmp (line, "[Amiga]", 7) == 0)
-		n--;
+	scan = eat_spaces (scan);
+	for (; i < N_FIELDS; i++) {
+		field_end = strchr (scan, ' ');
+		if (field_end == NULL || (i + 1) == N_FIELDS) {
+			field_end = scan + strlen(scan);
+		}
 
-	field = eat_spaces (line);
-	for (i = 0; i < n; i++) {
-		field = strchr (field, ' ');
-		field = eat_spaces (field);
+		fields[i] = g_strndup (scan, field_end - scan);
+		scan = eat_spaces (field_end);
 	}
 
-	return field;
+	return fields;
 }
 
 static void
@@ -181,15 +174,14 @@ process_line (char     *line,
 	fdata = file_data_new ();
 
 	fields = split_line_lha (line);
-	fdata->size = g_ascii_strtoull (fields[2], NULL, 10);
-	fdata->modified = mktime_from_string (fields[4],
-					      fields[5],
-					      fields[6]);
-	g_strfreev (fields);
+	fdata->size = g_ascii_strtoull (fields[FIELD_SIZE], NULL, 10);
+	fdata->modified = mktime_from_string (fields[FIELD_MONTH],
+					      fields[FIELD_DAY],
+					      fields[FIELD_TIME_OR_YEAR]);
 
 	/* Full path */
 
-	name_field = get_last_field_lha (line);
+	name_field = fields[FIELD_FILENAME];
 
 	if (name_field && *name_field == '/') {
 		fdata->full_path = g_strdup (name_field);
@@ -199,6 +191,8 @@ process_line (char     *line,
 		fdata->original_path = fdata->full_path + 1;
 	}
 
+	g_strfreev (fields);
+
 	fdata->link = NULL;
 
 	fdata->dir = line[0] == 'd';
diff --git a/src/fr-command-rar.c b/src/fr-command-rar.c
index 6bb70cd..880bfe9 100644
--- a/src/fr-command-rar.c
+++ b/src/fr-command-rar.c
@@ -39,6 +39,10 @@
 #include "fr-error.h"
 #include "rar-utils.h"
 
+
+#define IS_OUTPUT_TYPE(comm, type) ((comm)->output_type & (type))
+
+
 static void fr_command_rar_class_init  (FrCommandRarClass *class);
 static void fr_command_rar_init        (FrCommand         *afile);
 static void fr_command_rar_finalize    (GObject           *object);
@@ -150,6 +154,18 @@ attribute_field_with_space (const char *line)
 	return ((line[0] != ' ') && (line[1] == ' '));
 }
 
+static gboolean
+attr_field_is_dir (const char   *attr_field,
+                   FrCommandRar *rar_comm)
+{
+        if ((attr_field[0] == 'd') ||
+            (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5) && attr_field[3] == 'D') ||
+            (! IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5) && attr_field[1] == 'D'))
+                return TRUE;
+
+        return FALSE;
+}
+
 static void
 parse_name_field (char         *line,
 		  FrCommandRar *rar_comm)
@@ -163,10 +179,22 @@ parse_name_field (char         *line,
 
 	fdata->encrypted = (line[0] == '*') ? TRUE : FALSE;
 
-	if (rar_comm->output_type == FR_COMMAND_RAR_TYPE_RAR5)
+	if (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5)) {
+		int field_num = attribute_field_with_space (line) ? 9 : 8;
+		const char *field;
+
+		/* in RAR7 format, directories have a blank CRC32, not the
+		 * "????????" of the RAR5 format */
+		if (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR7)) {
+			field = get_last_field (line, field_num - 8);
+			if (attr_field_is_dir (field, rar_comm))
+				field_num--;
+		}
+
+		field = get_last_field (line, field_num);
 		/* rar-5 output adds trailing spaces to short file names :( */
-		name_field = g_strchomp (g_strdup (get_last_field (line, attribute_field_with_space (line) ? 9 : 8)));
-	else
+		name_field = field ? g_strchomp (g_strdup (field)) : NULL;
+	} else
 		name_field = g_strdup (line + 1);
 
 	if (name_field == NULL)
@@ -187,18 +215,6 @@ parse_name_field (char         *line,
 	g_free (name_field);
 }
 
-static gboolean
-attr_field_is_dir (const char   *attr_field,
-                   FrCommandRar *rar_comm)
-{
-        if ((attr_field[0] == 'd') ||
-            (rar_comm->output_type == FR_COMMAND_RAR_TYPE_RAR5 && attr_field[3] == 'D') ||
-            (rar_comm->output_type != FR_COMMAND_RAR_TYPE_RAR5 && attr_field[1] == 'D'))
-                return TRUE;
-
-        return FALSE;
-}
-
 static void
 process_line (char     *line,
 	      gpointer  data)
@@ -213,7 +229,12 @@ process_line (char     *line,
 		int version = 0;
 
 		if (sscanf (line, "RAR %d.", &version) == 1 || sscanf (line, "UNRAR %d.", &version) == 1) {
-			rar_comm->output_type = (version >= 5) ? FR_COMMAND_RAR_TYPE_RAR5 : FR_COMMAND_RAR_TYPE_RAR4;
+			if (version >= 7)
+				rar_comm->output_type = FR_COMMAND_RAR_TYPE_RAR7;
+			else if (version >= 5)
+				rar_comm->output_type = FR_COMMAND_RAR_TYPE_RAR5;
+			else
+				rar_comm->output_type = FR_COMMAND_RAR_TYPE_RAR4;
 
 			if (version > 5)
 				date_newstyle = TRUE;
@@ -230,7 +251,7 @@ process_line (char     *line,
 		}
 		else if (strncmp (line, "--------", 8) == 0) {
 			rar_comm->list_started = TRUE;
-			if (rar_comm->output_type != FR_COMMAND_RAR_TYPE_RAR5)
+			if (! IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5))
 			    rar_comm->rar4_odd_line = TRUE;
 		}
 		else if (strncmp (line, "Volume ", 7) == 0)
@@ -243,17 +264,17 @@ process_line (char     *line,
 		return;
 	}
 
-	if (rar_comm->rar4_odd_line || rar_comm->output_type == FR_COMMAND_RAR_TYPE_RAR5)
+	if (rar_comm->rar4_odd_line || IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5))
 		parse_name_field (line, rar_comm);
 
-	if (! rar_comm->rar4_odd_line) {
+	if (! rar_comm->rar4_odd_line && rar_comm->fdata && rar_comm->fdata->full_path) {
 		FileData   *fdata;
 		const char *size_field, *ratio_field, *date_field, *time_field, *attr_field;
 		int n_fields;
 
-		if (rar_comm->output_type == FR_COMMAND_RAR_TYPE_RAR5)
+		if (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5))
 			n_fields = 6 + (attribute_field_with_space (line) != 0);
-		else if (rar_comm->output_type == FR_COMMAND_RAR_TYPE_UNRAR_FREE)
+		else if (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_UNRAR_FREE))
 			n_fields = 4;
 		else
 			n_fields = 6;
@@ -272,7 +293,7 @@ process_line (char     *line,
 			parse_name_field (line, rar_comm);
 		}
 		else {
-			if (rar_comm->output_type == FR_COMMAND_RAR_TYPE_RAR5) {
+			if (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5)) {
 				int offset = attribute_field_with_space (line) ? 1 : 0;
 
 				size_field = fields[1+offset];
@@ -281,7 +302,7 @@ process_line (char     *line,
 				time_field = fields[5+offset];
 				attr_field = fields[0+offset];
 			}
-			else if (rar_comm->output_type == FR_COMMAND_RAR_TYPE_UNRAR_FREE) {
+			else if (IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_UNRAR_FREE)) {
 				size_field = fields[0];
 				date_field = fields[1];
 				time_field = fields[2];
@@ -336,7 +357,7 @@ process_line (char     *line,
 		}
 	}
 
-	if (rar_comm->output_type != FR_COMMAND_RAR_TYPE_RAR5)
+	if (! IS_OUTPUT_TYPE (rar_comm, FR_COMMAND_RAR_TYPE_RAR5))
 		rar_comm->rar4_odd_line = ! rar_comm->rar4_odd_line;
 }
 
@@ -676,7 +697,12 @@ fr_command_rar_handle_error (FrCommand   *comm,
 			volume_filename = g_path_get_basename (line + strlen ("Cannot find volume "));
 			error->gerror = g_error_new (FR_ERROR, error->status, _("Could not find the volume: %s"), volume_filename);
 			g_free (volume_filename);
-			break;
+
+			/* RAR7 complains about missing volume for incorrect passwords
+			 * as well, so don't make this a definite error in case we also
+			 * had an incorrect password one earlier */
+			if (! IS_OUTPUT_TYPE (FR_COMMAND_RAR (comm), FR_COMMAND_RAR_TYPE_RAR7))
+				break;
 		}
 	}
 }
diff --git a/src/fr-command-rar.h b/src/fr-command-rar.h
index 185d24e..ab4e12d 100644
--- a/src/fr-command-rar.h
+++ b/src/fr-command-rar.h
@@ -40,9 +40,11 @@ typedef struct _FrCommandRarClass  FrCommandRarClass;
 
 typedef enum
 {
-	FR_COMMAND_RAR_TYPE_RAR4 = 0,
-	FR_COMMAND_RAR_TYPE_RAR5,
-	FR_COMMAND_RAR_TYPE_UNRAR_FREE,
+	FR_COMMAND_RAR_TYPE_RAR4 = 1<<0,
+	FR_COMMAND_RAR_TYPE_RAR5 = 1<<1,
+	FR_COMMAND_RAR_TYPE_UNRAR_FREE = 1<<2,
+	/* RAR5 + empty CRC for directories */
+	FR_COMMAND_RAR_TYPE_RAR7 = (1<<3) | FR_COMMAND_RAR_TYPE_RAR5,
 } FrCommandRarType;
 
 struct _FrCommandRar
diff --git a/src/fr-command-rpm.c b/src/fr-command-rpm.c
index 90e5954..ab6ca39 100644
--- a/src/fr-command-rpm.c
+++ b/src/fr-command-rpm.c
@@ -208,7 +208,7 @@ fr_command_rpm_extract (FrCommand  *comm,
 
 	cmd = g_string_new ("rpm2cpio < ");
 	g_string_append (cmd, comm->e_filename);
-	g_string_append (cmd, " | cpio -idu");
+	g_string_append (cmd, " | cpio -idu --no-absolute-filenames");
 	for (scan = file_list; scan; scan = scan->next) {
 		g_string_append (cmd, " ");
 		char *filename = g_shell_quote (scan->data);
diff --git a/src/fr-window.c b/src/fr-window.c
index e86f7e0..d1ce30c 100644
--- a/src/fr-window.c
+++ b/src/fr-window.c
@@ -1493,8 +1493,12 @@ fr_window_populate_file_list (FrWindow  *window,
 			} else {
 				GDateTime *date_time;
 				date_time = g_date_time_new_from_unix_local (fdata->modified);
-				s_time = g_date_time_format (date_time, _("%d %B %Y, %H:%M"));
-				g_date_time_unref (date_time);
+				if (! date_time) {
+					s_time = g_strdup ("");
+				} else {
+					s_time = g_date_time_format (date_time, _("%d %B %Y, %H:%M"));
+					g_date_time_unref (date_time);
+				}
 			}
 
 			gtk_list_store_set (window->priv->list_store, &iter,
@@ -1522,8 +1526,12 @@ fr_window_populate_file_list (FrWindow  *window,
 
 			s_size = g_format_size (fdata->size);
 			date_time = g_date_time_new_from_unix_local (fdata->modified);
-			s_time = g_date_time_format (date_time, _("%d %B %Y, %H:%M"));
-			g_date_time_unref (date_time);
+			if (! date_time) {
+				s_time = g_strdup("");
+			} else {
+				s_time = g_date_time_format (date_time, _("%d %B %Y, %H:%M"));
+				g_date_time_unref (date_time);
+			}
 			desc = g_content_type_get_description (fdata->content_type);
 
 			gtk_list_store_set (window->priv->list_store, &iter,
diff --git a/src/java-utils.c b/src/java-utils.c
index 1ea7783..6000eca 100644
--- a/src/java-utils.c
+++ b/src/java-utils.c
@@ -207,6 +207,7 @@ load_constant_pool_utfs (JavaClassFile *cfile)
 			txt->length = GUINT16_FROM_BE (txt->length);
 			txt->str = g_new0 (char, txt->length);
 			if (read (cfile->fd, txt->str, txt->length) == -1) {
+				g_free (txt->str);
 				g_free (txt);
 				return;	/* error while reading */
 			}
EOF

if ! grep -q "1002_upstream_fixes_rar7_and_security.patch" debian/patches/series; then
    echo "1002_upstream_fixes_rar7_and_security.patch" >> debian/patches/series
fi

# Añadir nota al changelog de Debian
DEBEMAIL="soporte@local" DEBFULLNAME="Reparacion Local" \
dch -l "+rar7fix" "Soluciona cuelgue con RAR 7.x por columna vacía de CRC32 en directorios (commits 51a2a84b, 3565a5f2, bfad4da5) y parches upstream de seguridad/estabilidad."

echo ""
echo "[5/6] Compilando paquetes Debian oficiales (.deb)..."
sudo -u "$REAL_USER" dpkg-buildpackage -b -uc -us

echo ""
echo "[6/6] Instalando los paquetes corregidos en el sistema..."
cd "$WORK_DIR"
dpkg -i engrampa_*.deb engrampa-common_*.deb

echo ""
echo "[+] Limpiando directorio temporal de compilación..."
rm -rf "$WORK_DIR"

echo "[+] Limpiando wrappers temporales del usuario (si existen)..."
if [ -f "$REAL_HOME/.local/bin/rar" ] && grep -q "real_cmd = \"/usr/bin/rar\"" "$REAL_HOME/.local/bin/rar"; then
    rm -f "$REAL_HOME/.local/bin/rar" "$REAL_HOME/.local/bin/unrar"
    echo "    - Wrappers rar/unrar de usuario retirados (reemplazados por soporte nativo)."
fi
if [ -f "$REAL_HOME/.local/bin/engrampa" ]; then
    rm -f "$REAL_HOME/.local/bin/engrampa"
    echo "    - Wrapper engrampa de usuario retirado."
fi
if [ -f "$REAL_HOME/.local/share/applications/engrampa.desktop" ]; then
    rm -f "$REAL_HOME/.local/share/applications/engrampa.desktop"
    update-desktop-database "$REAL_HOME/.local/share/applications" 2>/dev/null || true
    echo "    - Entrada desktop personalizada de usuario sincronizada."
fi

echo ""
echo "=========================================================="
echo " ¡Reparación nativa completada con éxito!"
echo " Versión instalada:"
engrampa --version || true
echo "=========================================================="
