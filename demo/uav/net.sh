#!/bin/sh

ip link add link eth0 name uav0 type vlan id 1
ip addr add 10.0.0.100/24 dev uav0
ip link set dev uav0 up

iptables -I INPUT -s demo_station_1 -j REJECT