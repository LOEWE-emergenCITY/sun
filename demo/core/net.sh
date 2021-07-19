#!/bin/sh

ip link add link eth0 name uav0 type vlan id 1 
ip link set uav0 up

ip link add link eth2 name qgc0 type vlan id 2
ip link set qgc0 up
