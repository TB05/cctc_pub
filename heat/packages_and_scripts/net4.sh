#!/bin/bash

# --- install metasploitable3
echo "Setup Metasploitable3"
apt-get install -y curl git
git clone https://github.com/rapid7/metasploitable3.git
curl -L https://omnitruck.chef.io/install.sh | bash -s -- -v 13.8.5
mkdir /var/chef

cat > "/metasploitable3/chef/cookbooks/ms3.json" << __EOF__
{
  "run_list": [
    "metasploitable::users",
    "metasploitable::mysql",
    "metasploitable::apache_continuum",
    "metasploitable::apache",
    "metasploitable::php_545",
    "metasploitable::phpmyadmin",
    "metasploitable::proftpd",
    "metasploitable::docker",
    "metasploitable::samba",
    "metasploitable::sinatra",
    "metasploitable::unrealircd",
    "metasploitable::chatbot",
    "metasploitable::payroll_app",
    "metasploitable::readme_app",
    "metasploitable::cups",
    "metasploitable::drupal",
    "metasploitable::knockd",
    "metasploitable::iptables",
    "metasploitable::flags"
  ]
}

__EOF__

chef-solo -j /metasploitable3/chef/cookbooks/ms3.json --config-option cookbook_path=/metasploitable3/chef/cookbooks

# --- setup SSH
echo "SETUP SSH"
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

systemctl restart ssh

# -- setup TCP Offload
echo "SETUP TCP Offload"
/sbin/ethtool -K ens3 tx off sg off tso off

chmod +x /etc/network/if-up.d/tcpoffload
/etc/network/if-up.d/tcpoffload

# Fix routing for openvpn
#echo "Fix routing for OpenVPN"
#echo "# The interface for ens3" >> /etc/network/interfaces
#echo "auto ens3" >> /etc/network/interfaces
#echo "iface ens3 inet dhcp" >> /etc/network/interfaces
#echo "up route add -net 192.168.0.0 netmask 255.255.0.0 gw 10.2.0.254" >> /etc/network/interfaces

# User Creation
echo "CREATE USER"
useradd $user -m -U -s /bin/bash
usermod -aG sudo alexander
echo "root:$password" | chpasswd
echo "$user:$password" | chpasswd

reboot