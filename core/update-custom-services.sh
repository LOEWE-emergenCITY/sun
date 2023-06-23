#!/bin/sh

DIR="/shared/myservices"
if [ -d "$DIR" ]; then  
  # check if custom_services_dir already added to core.conf
  grep -q "^custom_services_dir" /etc/core/core.conf
  if [ $? -eq 0 ]; then
    echo "custom_services_dir already added to core.conf"
  else    
    echo "Adding ${DIR} to custom services dir of core"
    echo custom_services_dir = /root/.core/myservices,/shared/myservices >> /etc/core/core.conf
  fi
else
  ###  Control will jump here if $DIR does NOT exists ###
  grep -q "^custom_services_dir" /etc/core/core.conf
  if [ $? -eq 0 ]; then
    echo "custom_services_dir already added to core.conf"
  else
    echo custom_services_dir = /root/.core/myservices >> /etc/core/core.conf
  fi
fi


DIR="/shared/custom_services"
if [ -d "$DIR" ]; then  
  # check if custom_config_services_dir already added to core.conf
  grep -q "^custom_config_services_dir" /etc/core/core.conf
  if [ $? -eq 0 ]; then
    echo "custom_config_services_dir already added to core.conf"
  else
    echo "Adding custom_config_services_dir to core.conf"
    echo custom_config_services_dir = /root/.coregui/custom_services,/shared/custom_services >> /etc/core/core.conf
  fi  
else
  ###  Control will jump here if $DIR does NOT exists ###
  grep -q "^custom_config_services_dir" /etc/core/core.conf
  if [ $? -eq 0 ]; then
    echo "custom_config_services_dir already added to core.conf"
  else
    echo custom_config_services_dir = /root/.coregui/custom_services >> /etc/core/core.conf
  fi
fi