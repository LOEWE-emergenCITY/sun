#!/bin/sh

#set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <mission_folder>"
    exit 1
fi

cat templates/docker-compose.yml.TEMPLATE | sed -e "s+SHAREDDIR+./$1+g" >docker-compose.yml

docker-compose build
docker-compose up -d --remove-orphans
sleep 5
# connect core gui: password netsim
#ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -Y -p 2022 root@localhost core-pygui -s 1 &
echo "ground station: vnc://127.0.0.1:15901"
echo "core network: vnc://127.0.0.1:15902"
echo "core network: ssh://root@127.0.0.1:2022"
sleep 2
BASE_X=$(docker exec -it sun_core_1 core-pos uav0 | egrep -ex | awk '{print $2}' | sed 's/,*\r*$//')
BASE_Y=$(docker exec -it sun_core_1 core-pos uav0 | egrep -ey | awk '{print $2}' | sed 's/,*\r*$//')
docker exec -it sun_core_1 core-cli node edit -i 4 -p $BASE_X,$BASE_Y -ic /root/.coregui/icons/uav.png
sleep 1

if [ -f "$1/px4-params.txt" ]; then
    echo "Loading parameters from $1/px4-params.txt"
    for i in $(cat $1/px4-params.txt | grep -v "^#" | grep "="); do
        PARAM=$(echo $i | sed -e 's/=/ /g')
        docker exec -it sun_uav_1 /root/PX4-Autopilot/build/px4_sitl_default/bin/px4-param set $PARAM
        #echo $PARAM
        sleep 1
    done
else
    echo "File $1/px4-params.txt not found, not setting extra PX4 parameters"

fi

if [ -f "$1/autostart.sh" ]; then
    echo "Running $1/autostart.sh"
    bash $1/autostart.sh
fi
docker exec -it sun_uav_1 python3 /usr/local/bin/gz_pose.py

# mutli node mesh setup: babeld -D -C 'redistribute metric 256' eth0
#tail -f /dev/null

docker-compose stop
docker-compose rm -f core
docker-compose rm -f uav
docker-compose rm -f station
