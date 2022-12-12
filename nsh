#!/bin/sh

if [ -z "$1" ]; then
    echo "Usage: $0 <uav|core|station|<coreemu virtual node name>>"
    exit 1
fi

if [ "$1" = "uav" ]; then
    docker exec -it sun_uav_1 /bin/bash
elif [ "$1" = "core" ]; then
    docker exec -it sun_core_1 /bin/bash
elif [ "$1" = "station" ]; then
    docker exec -it sun_station_1 /bin/bash
else
    docker exec -it sun_core_1 cbash $1
fi
