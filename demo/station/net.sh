#!/bin/sh

ip link add link eth1 name qgc0 type vlan id 2
ip addr add 10.0.0.1/24 dev qgc0
ip link set dev qgc0 up

sysctl -w net.ipv6.conf.qgc0.disable_ipv6=0

iptables -I INPUT -s demo_uav_1 -j REJECT