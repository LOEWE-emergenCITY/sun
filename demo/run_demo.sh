#!/bin/sh

docker compose up -d 
sleep 5
# connect core gui: password netsim
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -Y -p 2022 root@localhost core-pygui -s 1 &
sleep 1
docker exec -it demo_core_1 core-cli node edit -i 4 -p 100,100 -ic /root/.coregui/icons/uav.png
sleep 1
docker exec -it demo_uav_1 python3 /usr/local/bin/gz_pose.py

#tail -f /dev/null

docker compose stop
docker compose rm -f core