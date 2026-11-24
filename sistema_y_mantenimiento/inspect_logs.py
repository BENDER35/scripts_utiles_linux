import os
import subprocess
import glob

def run(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return res.stdout.strip() + "\n" + res.stderr.strip()
    except Exception as e:
        return f"Error executing '{cmd}': {str(e)}"

print("=== 1. JOURNALCTL & SYSLOG ===")
print("--- Journalctl Priority 3 (ERR) ---")
print(run("journalctl -p 3 -b 0 -n 30 --no-pager"))
print("--- Journalctl Priority 4 (WARNING) ---")
print(run("journalctl -p 4 -b 0 -n 20 --no-pager"))
print("--- /var/log/syslog (recent errors) ---")
print(run("grep -i -E 'error|fail|critical' /var/log/syslog | tail -n 20"))

print("\n=== 2. SNAP & FLATPAK ===")
print("--- Snap daemon logs ---")
print(run("journalctl -u snapd -n 20 --no-pager"))
print("--- Snap changes ---")
print(run("snap changes 2>&1 | tail -n 15"))
print("--- Flatpak repair / check ---")
print(run("flatpak status 2>&1 || flatpak list 2>&1"))
print("--- Journalctl Flatpak ---")
print(run("journalctl -b 0 | grep -i flatpak | tail -n 20"))

print("\n=== 3. XFCE & DESKTOP (xsession-errors) ===")
print("--- .xsession-errors tail ---")
if os.path.exists(os.path.expanduser("~/.xsession-errors")):
    print(run("grep -i -E 'error|warn|fail|critical' ~/.xsession-errors | tail -n 30"))
else:
    print(".xsession-errors not found")
print("--- Journalctl XFCE ---")
print(run("journalctl -b 0 | grep -i -E 'xfce|xfwm|xfdesktop|panel' | grep -i -E 'error|warn|fail' | tail -n 20"))

print("\n=== 4. FIREFOX & THUNDERBIRD ===")
print("--- Firefox Crash Reports ---")
print(run("ls -la ~/.mozilla/firefox/*.default*/crashes/store/ 2>/dev/null || true"))
print(run("journalctl -b 0 | grep -i firefox | grep -i -E 'error|warn|fail' | tail -n 20"))
print("--- Thunderbird Crash Reports ---")
print(run("ls -la ~/.thunderbird/*.default*/crashes/store/ 2>/dev/null || true"))
print(run("journalctl -b 0 | grep -i thunderbird | grep -i -E 'error|warn|fail' | tail -n 20"))

print("\n=== 5. GOOGLE CHROME ===")
print("--- Chrome Crash Reports / Journalctl ---")
print(run("ls -la ~/.config/google-chrome/Crash* 2>/dev/null || true"))
print(run("journalctl -b 0 | grep -i chrome | grep -i -E 'error|warn|fail' | tail -n 20"))

print("\n=== 6. ANYDESK & RETROARCH ===")
print("--- AnyDesk Logs ---")
print(run("ls -la ~/.anydesk/ /var/log/anydesk* 2>/dev/null || true"))
print(run("cat ~/.anydesk/anydesk.trace 2>/dev/null | grep -i -E 'error|warn|fail|critical' | tail -n 20 || true"))
print(run("cat /var/log/anydesk.log 2>/dev/null | grep -i -E 'error|warn|fail|critical' | tail -n 20 || true"))
print("--- RetroArch Logs ---")
print(run("ls -la ~/.config/retroarch/ 2>/dev/null || true"))
print(run("cat ~/.config/retroarch/retroarch.log 2>/dev/null | grep -i -E 'error|warn|fail|critical' | tail -n 20 || true"))

print("\n=== 7. SOFTWARE-PROPERTIES-GTK & GRUB ===")
print("--- Apt / Software-Properties Logs ---")
print(run("tail -n 30 /var/log/apt/term.log 2>/dev/null || true"))
print(run("journalctl -b 0 | grep -i software-properties | tail -n 20"))
print("--- GRUB logs & errors ---")
print(run("journalctl -b 0 | grep -i grub | tail -n 20"))
print(run("cat /var/log/boot.log 2>/dev/null | grep -i -E 'grub|error|fail' | tail -n 20 || true"))

