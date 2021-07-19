#!/bin/sh

ip link add link eth0 name uav0 type vlan id 1
ip addr add 10.0.1.2/24 dev uav0
ip link set dev uav0 up

route add -net 10.0.2.0/24 gw 10.0.1.1

iptables -I INPUT -s demo_station_1 -j REJECT