#!/bin/sh

ip link add link eth1 name qgc0 type vlan id 2
ip addr add 10.0.2.2/24 dev qgc0
ip link set dev qgc0 up

route add -net 10.0.1.0/24 gw 10.0.2.20

sysctl -w net.ipv6.conf.qgc0.disable_ipv6=0

iptables -I INPUT -s sun_uav_1 -j REJECT
