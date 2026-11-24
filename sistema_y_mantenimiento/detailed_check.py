import subprocess
import os
import glob

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return (res.returncode, res.stdout, res.stderr)
    except Exception as e:
        return (-1, "", str(e))

print("==================================================")
print("1. JOURNALCTL ERRORS & SYSTEM LOGS")
print("==================================================")
code, out, err = run_cmd("journalctl -p 3 -b 0 --no-pager -n 50")
print(out)

code, out, err = run_cmd("journalctl -b 0 --failed --no-pager")
print("FAILED UNITS:")
print(out if out else "No failed units.")

print("\n==================================================")
print("2. SYSLOG ERRORS")
print("==================================================")
code, out, err = run_cmd("grep -i -E 'error|failed|fault|critical|warning' /var/log/syslog | tail -n 40 2>/dev/null")
print(out if out else "Syslog check via journalctl fallback:")
if not out:
    code, out, err = run_cmd("journalctl -p 4 -b 0 -n 40 --no-pager")
    print(out)

print("\n==================================================")
print("3. FIREFOX LOGS & STATUS")
print("==================================================")
code, out, err = run_cmd("journalctl -b 0 | grep -i firefox | tail -n 30")
print("Journalctl firefox:")
print(out if out else "None")

# Check firefox snap / deb status
code, out, err = run_cmd("snap list firefox 2>&1")
print("Snap firefox status:", out)

# Check crash logs
crash_dirs = glob.glob(os.path.expanduser("~/.mozilla/firefox/*/crashes/store/"))
print("Firefox crash store files:", crash_dirs)

print("\n==================================================")
print("4. THUNDERBIRD LOGS & STATUS")
print("==================================================")
code, out, err = run_cmd("journalctl -b 0 | grep -i thunderbird | tail -n 30")
print("Journalctl thunderbird:")
print(out if out else "None")
code, out, err = run_cmd("snap list thunderbird 2>&1")
print("Snap thunderbird status:", out)

print("\n==================================================")
print("5. FLATPAK LOGS & REPAIR CHECK")
print("==================================================")
code, out, err = run_cmd("flatpak repair --dry-run 2>&1")
print("Flatpak repair dry-run:")
print(out)
code, out, err = run_cmd("flatpak list --unsupported 2>&1; flatpak list 2>&1")
print("Flatpak list:")
print(out[:500])

print("\n==================================================")
print("6. SNAP LOGS & SNAPD STATUS")
print("==================================================")
code, out, err = run_cmd("snap list 2>&1")
print("Installed snaps:")
print(out)
code, out, err = run_cmd("journalctl -u snapd -p 4 -n 30 --no-pager")
print("Snapd warnings/errors:")
print(out)

print("\n==================================================")
print("7. ANYDESK LOGS & SERVICE")
print("==================================================")
code, out, err = run_cmd("systemctl status anydesk --no-pager 2>&1")
print("Anydesk service status:")
print(out)
code, out, err = run_cmd("tail -n 30 /var/log/anydesk.trace 2>/dev/null || tail -n 30 ~/.anydesk/anydesk.trace 2>/dev/null")
print("AnyDesk trace log tail:")
print(out)

print("\n==================================================")
print("8. RETROARCH LOGS & CONFIG")
print("==================================================")
code, out, err = run_cmd("ls -la ~/.config/retroarch/ 2>&1")
print("RetroArch dir content:")
print(out)
code, out, err = run_cmd("journalctl -b 0 | grep -i retroarch | tail -n 30")
print("Journalctl RetroArch:")
print(out if out else "None in journalctl")

print("\n==================================================")
print("9. GOOGLE CHROME LOGS")
print("==================================================")
code, out, err = run_cmd("journalctl -b 0 | grep -i -E 'chrome|chromium' | tail -n 30")
print("Journalctl Chrome:")
print(out if out else "None in journalctl")

print("\n==================================================")
print("10. SOFTWARE-PROPERTIES-GTK & APT LOGS")
print("==================================================")
code, out, err = run_cmd("journalctl -b 0 | grep -i software-properties | tail -n 30")
print("Journalctl software-properties:")
print(out if out else "None in journalctl")

# Apt update check for PPA errors or repo errors
code, out, err = run_cmd("apt-cache policy 2>&1 | head -n 20")
print("APT policy sample:")
print(out)

print("\n==================================================")
print("11. XFCE LOGS")
print("==================================================")
code, out, err = run_cmd("journalctl -b 0 | grep -i -E 'xfce4|xfwm4|xfdesktop|lightdm' | grep -i -E 'error|warn|fail|critical' | tail -n 40")
print("Journalctl XFCE/Desktop errors:")
print(out if out else "None in journalctl")
if os.path.exists(os.path.expanduser("~/.xsession-errors")):
    code, out, err = run_cmd("grep -i -E 'error|fail|warning|critical' ~/.xsession-errors | tail -n 30")
    print("~/.xsession-errors sample:")
    print(out)

print("\n==================================================")
print("12. GRUB LOGS & CONFIG CHECK")
print("==================================================")
code, out, err = run_cmd("journalctl -b 0 | grep -i grub | tail -n 30")
print("Journalctl GRUB:")
print(out)
code, out, err = run_cmd("cat /etc/default/grub 2>&1")
print("/etc/default/grub:")
print(out)

