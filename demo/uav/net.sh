#!/bin/bash

source /shared/experiment.conf

if [[ $SCENARIO == uav_routed* ]]; then
    echo "Running UAV routed scenario"
    /net-routed.sh
else
    echo "Running UAV direct scenario"
    ip link add link eth0 name uav0 type vlan id 1
    ip addr add 10.0.0.100/24 dev uav0
    ip link set dev uav0 up
fi 
sysctl -w net.ipv6.conf.uav0.disable_ipv6=0 

iptables -I INPUT -s demo_station_1 -j REJECT