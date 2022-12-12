#!/bin/sh

DIR="/shared/myservices"
if [ -d "$DIR" ]; then  
  echo "Adding ${DIR} to custom services dir of core"
  echo custom_services_dir = /root/.core/myservices,/shared/myservices >> /etc/core/core.conf
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo custom_services_dir = /root/.core/myservices >> /etc/core/core.conf
fi


DIR="/shared/custom_services"
if [ -d "$DIR" ]; then  
  echo "Adding ${DIR} to custom services dir of core"
  echo custom_config_services_dir = /root/.coregui/custom_services,/shared/custom_services >> /etc/core/core.conf
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo custom_config_services_dir = /root/.coregui/custom_services >> /etc/core/core.conf
fi