import subprocess

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    return res.stdout + "\n" + res.stderr

print("Checking APT update / PPA issues...")
print(run_cmd("apt-get update --dry-run 2>&1 || true"))

print("\nChecking anydesk service PID file:")
print(run_cmd("cat /etc/systemd/system/anydesk.service 2>/dev/null || true"))

print("\nChecking GRUB env:")
print(run_cmd("grub-editenv /boot/grub/grubenv list 2>/dev/null || true"))

