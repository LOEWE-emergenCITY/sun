#!/bin/sh

ip link add link eth0 name uav0 type vlan id 1 
ip link set uav0 up

ip link add link eth2 name qgc0 type vlan id 2
#ip link add link eth0 name qgc0 type vlan id 2
ip link set qgc0 up

if test -f "/tmp/.X1-lock"; then
	  rm /tmp/.X1-lock
  	  rm /tmp/.X11-unix/X1
fi

/usr/bin/tightvncserver -geometry 1280x800 -depth 24 &