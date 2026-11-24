#!/usr/bin/env bash
# ==============================================================================
# Script de Diagnóstico y Reparación de Red para Máquinas Virtuales
# Compatible con: VMware Workstation, VirtualBox y QEMU / KVM
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[-] Este script debe ejecutarse con permisos de administrador (root)."
  echo "    Por favor ejecuta: sudo bash $0"
  exit 1
fi

echo "=========================================================="
echo "    Iniciando Reparación de Red para Hipervisores"
echo "=========================================================="

# 1. Habilitar Reenvío IP (IP Forwarding) en el Kernel
echo "[+] 1. Asegurando IP Forwarding en el kernel..."
sysctl -w net.ipv4.ip_forward=1 >/dev/null
cat << 'EOF' > /etc/sysctl.d/99-vm-routing.conf
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
EOF
sysctl -p /etc/sysctl.d/99-vm-routing.conf >/dev/null

# 2. Corregir Servidores DNS en el DHCP de VMware (vmnet8 NAT)
# Por defecto VMware asigna como DNS su propia IP (172.16.217.2), la cual falla
# con systemd-resolved en Ubuntu moderno (no soporta EDNS0/DNSSEC).
VMWARE_DHCP_CONF="/etc/vmware/vmnet8/dhcpd/dhcpd.conf"
if [ -f "$VMWARE_DHCP_CONF" ]; then
    echo "[+] 2. Configurando servidores DNS directos (1.1.1.1, 8.8.8.8) en VMware NAT..."
    cp "$VMWARE_DHCP_CONF" "${VMWARE_DHCP_CONF}.bak"
    # Reemplazar la asignación de DNS 172.16.217.2 por DNS públicos estables
    sed -i 's/option domain-name-servers .*/option domain-name-servers 1.1.1.1, 8.8.8.8, 1.0.0.1;/' "$VMWARE_DHCP_CONF"
fi

# 3. Ajustar Reglas de Firewall (iptables / nftables) para MSS Clamping y Forwarding
# Si Cloudflare WARP o la VPN tiene MTU reducida (ej. 1300), TCP MSS Clamping evita
# que las conexiones HTTPS de Ubuntu se queden colgadas por paquetes demasiado grandes.
echo "[+] 3. Aplicando TCP MSS Clamping y permisos de reenvío en el firewall..."
if command -v iptables >/dev/null 2>&1; then
    # Clamping de MSS al MTU del trayecto
    iptables -t mangle -C FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu 2>/dev/null || \
    iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu

    # Permitir reenvío para interfaces virtuales de VMware, QEMU y VirtualBox
    for iface in vmnet1 vmnet8 virbr0 vboxnet0; do
        iptables -C FORWARD -i "$iface" -j ACCEPT 2>/dev/null || iptables -A FORWARD -i "$iface" -j ACCEPT 2>/dev/null || true
        iptables -C FORWARD -o "$iface" -m state --state RELATED,ESTABLISHED -j ACCEPT 2>/dev/null || iptables -A FORWARD -o "$iface" -m state --state RELATED,ESTABLISHED -j ACCEPT 2>/dev/null || true
    done
fi

# 4. Reiniciar servicios de red de VMware
echo "[+] 4. Reiniciando demonios de red de VMware..."
if [ -x "/usr/bin/vmware-networks" ]; then
    /usr/bin/vmware-networks --stop 2>/dev/null || true
    sleep 1
    /usr/bin/vmware-networks --start 2>/dev/null || true
elif systemctl is-active --quiet vmware; then
    systemctl restart vmware
fi

# 5. Reiniciar red de QEMU / KVM (libvirt) si está instalada
if command -v virsh >/dev/null 2>&1 && systemctl is-active --quiet libvirtd; then
    echo "[+] 5. Verificando red default de QEMU/libvirt..."
    virsh net-destroy default 2>/dev/null || true
    virsh net-start default 2>/dev/null || true
fi

echo "=========================================================="
echo " [OK] Reparación completada con éxito."
echo ""
echo " CONSEJOS IMPORTANTES PARA TUS MÁQUINAS VIRTUALES:"
echo " 1) Si usas Cloudflare WARP:"
echo "    Si la VM sigue sin conexión tras esto, desactiva WARP temporalmente"
echo "    con: warp-cli disconnect"
echo ""
echo " 2) En VMware para máquinas Ubuntu / Lubuntu modernas:"
echo "    - En la configuración de la VM (Network Adapter), selecciona siempre: NAT."
echo "    - Si el adaptador de red en el archivo .vmx es 'vmxnet3', cámbialo a:"
echo "      ethernet0.virtualDev = \"e1000e\""
echo "      (vmxnet3 en Linux moderno sufre un error de checksum offloading)."
echo ""
echo " 3) En VirtualBox:"
echo "    - Cambia el adaptador de 'Modo Puente (Bridged)' a 'NAT'."
echo "    - El adaptador en Modo Puente falla sobre tarjetas Wi-Fi (wlp1s0)."
echo "=========================================================="
