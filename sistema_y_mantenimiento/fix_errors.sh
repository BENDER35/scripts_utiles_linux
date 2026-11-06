#!/bin/bash
# Script to fix detected system errors (requires root permissions)
# Run as: sudo ./fix_errors.sh

set -e

echo "=== System Error Correction Script ==="

# 1. Fix GRUB environment block corruption (grub-initrd-fallback.service failure)
echo "Checking GRUB environment block /boot/grub/grubenv..."
if [ -f /boot/grub/grubenv ]; then
    echo "Recreating /boot/grub/grubenv to resolve 'Invalid argument' read errors..."
    rm -f /boot/grub/grubenv
    grub-editenv /boot/grub/grubenv create
    echo "GRUB environment block recreated successfully."
    
    echo "Attempting to restart grub-initrd-fallback.service..."
    if systemctl restart grub-initrd-fallback.service; then
        echo "Service grub-initrd-fallback.service restarted successfully!"
        systemctl status grub-initrd-fallback.service
    else
        echo "WARNING: Failed to restart grub-initrd-fallback.service. Checking logs..."
        journalctl -u grub-initrd-fallback.service -n 10 --no-pager
    fi
else
    echo "/boot/grub/grubenv not found. Creating it..."
    grub-editenv /boot/grub/grubenv create
fi

# 2. Clear stale Firefox/Thunderbird lock files
echo "Checking for stale lock files in user Firefox and Thunderbird profile directories..."
# We can search in all user homes (e.g. /home/*)
for user_home in /home/*; do
    if [ -d "$user_home" ]; then
        # Firefox snaps
        find "$user_home/snap/firefox/common/.mozilla/firefox" -name ".parentlock" -type f 2>/dev/null | while read -r lock_file; do
            # Check if firefox is running for this user
            username=$(basename "$user_home")
            if ! pgrep -u "$username" -x "firefox" > /dev/null; then
                echo "Removing stale Firefox lock file for user $username: $lock_file"
                rm -f "$lock_file"
            fi
        done
        # Thunderbird snaps
        find "$user_home/snap/thunderbird/common/.thunderbird" -name ".parentlock" -type f 2>/dev/null | while read -r lock_file; do
            # Check if thunderbird is running for this user
            username=$(basename "$user_home")
            if ! pgrep -u "$username" -x "thunderbird" > /dev/null; then
                echo "Removing stale Thunderbird lock file for user $username: $lock_file"
                rm -f "$lock_file"
            fi
        done
    fi
done

echo "Correction process completed!"
