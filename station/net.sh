#!/bin/bash

source /shared/experiment.conf

if [[ $SCENARIO == uav_routed* ]]; then
    echo "Running UAV routed scenario"
    /net-routed.sh
else
    echo "Running UAV direct scenario"
    ip link add link eth1 name qgc0 type vlan id 2
    #ip link add link eth0 name qgc0 type vlan id 2
    ip addr add 10.0.0.1/24 dev qgc0
    ip link set dev qgc0 up
fi

sysctl -w net.ipv6.conf.qgc0.disable_ipv6=0

iptables -I INPUT -s sun_uav_1 -j REJECT
