#!/bin/sh

docker-compose up -d --remove-orphans
sleep 5
# connect core gui: password netsim
#ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -Y -p 2022 root@localhost core-pygui -s 1 &
echo "ground station: vnc://127.0.0.1:15901"
echo "core network: vnc://127.0.0.1:15902"
echo "core network: ssh://root@127.0.0.1:2022"
sleep 2
BASE_X=$(docker exec -it demo_core_1 core-pos uav0 | egrep -ex | awk '{print $2}' | sed 's/,*\r*$//')
BASE_Y=$(docker exec -it demo_core_1 core-pos uav0 | egrep -ey | awk '{print $2}' | sed 's/,*\r*$//')
docker exec -it demo_core_1 core-cli node edit -i 4 -p $BASE_X,$BASE_Y -ic /root/.coregui/icons/uav.png
sleep 1
docker exec -it demo_uav_1 /root/PX4-Autopilot/build/px4_sitl_default/bin/px4-param set NAV_RCL_ACT 0
sleep 1
docker exec -it demo_uav_1 /root/PX4-Autopilot/build/px4_sitl_default/bin/px4-param set MPC_XY_CRUISE 20
sleep 1
docker exec -it demo_uav_1 /root/PX4-Autopilot/build/px4_sitl_default/bin/px4-param set MPC_XY_VEL_MAX 20
sleep 1
docker exec -it demo_uav_1 python3 /usr/local/bin/gz_pose.py

# mutli node mesh setup: babeld -D -C 'redistribute metric 256' eth0
#tail -f /dev/null

docker-compose stop
docker-compose rm -f core
docker-compose rm -f uav
docker-compose rm -f station