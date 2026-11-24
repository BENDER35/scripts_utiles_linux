import os
import glob
import subprocess

print("=== User-level Fixes ===")

# 1. Clean Chrome old crash reports
chrome_crashes = os.path.expanduser("~/.config/google-chrome/Crash Reports/completed/*")
removed_chrome = 0
for f in glob.glob(chrome_crashes):
    try:
        os.remove(f)
        removed_chrome += 1
    except Exception as e:
        print(f"Error removing {f}: {e}")
print(f"Cleaned {removed_chrome} Chrome completed crash report files.")

# 2. Ensure RetroArch directory structure exists
retroarch_dir = os.path.expanduser("~/.config/retroarch")
if not os.path.exists(retroarch_dir):
    os.makedirs(retroarch_dir, exist_ok=True)
    print(f"Created RetroArch configuration directory: {retroarch_dir}")
else:
    print(f"RetroArch configuration directory exists: {retroarch_dir}")

# 3. Variety wallpaper configuration check
variety_conf = os.path.expanduser("~/.config/variety/variety.conf")
if os.path.exists(variety_conf):
    print(f"Found variety config file: {variety_conf}")

