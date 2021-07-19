#!/bin/sh

docker compose up -d 
sleep 3
docker exec -it demo_uav_1 python3 /usr/local/bin/gz_pose.py

# connect core gui: password netsim
# ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -Y -p 2022 root@localhost core-gui

docker compose stop
docker compose rm -f core