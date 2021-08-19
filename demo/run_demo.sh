#!/bin/sh

docker-compose up -d --remove-orphans
sleep 5
# connect core gui: password netsim
#ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -Y -p 2022 root@localhost core-pygui -s 1 &
echo "ground station: vnc://127.0.0.1:15901"
echo "core network: vnc://127.0.0.1:15902"
echo "core network: ssh://root@127.0.0.1:2022"
sleep 1
docker exec -it demo_core_1 core-cli node edit -i 4 -p 100,100 -ic /root/.coregui/icons/uav.png
sleep 1
docker exec -it demo_uav_1 python3 /usr/local/bin/gz_pose.py

# mutli node mesh setup: babeld -D -C 'redistribute metric 256' eth0
#tail -f /dev/null

docker-compose stop
docker-compose rm -f core