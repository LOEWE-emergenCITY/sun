#!/usr/bin/python3

import sys
import time
import os
# display out put line by line
import subprocess

# local gazebo
proc = subprocess.Popen(
    ['gz', 'topic', '-e', '/gazebo/default/pose/info'], stdout=subprocess.PIPE)

# dockered gazebo
# proc = subprocess.Popen(
# ['docker', 'exec', '-it', 'px4', 'bash', '-c', 'gz topic -e /gazebo/default/pose/info'], stdout=subprocess.PIPE)

initial_pos = subprocess.run(['core-pos', 'uav0'], stdout=subprocess.PIPE)
for i in initial_pos.stdout.decode('utf-8').split('\n'):
    i = i.strip().rstrip(',')
    if i.startswith('x: '):
        base_x = float(i.split(': ')[1])
    if i.startswith('y: '):
        base_y = float(i.split(': ')[1])

print("Initial position: " + str(base_x) + " " + str(base_y))

wait_per_update_in_s = 0.2

scanning = False
x = 0.0
y = 0.0
z = 0.0

last_update = time.time()

print("capturing positions from gazebo...")
single_node = False
# works in python 3.0+
for line in proc.stdout:
    line = line.decode("utf-8").strip()
    # if scanning:
    #    print(line)
    if '"iris"' in line:
        x = 0.0
        y = 0.0
        z = 0.0
        if time.time() - last_update > wait_per_update_in_s:
            #print(line + "\r\n")
            scanning = True
    elif 'x:' in line and scanning:
        x = float(line.split(' ')[1])
    elif 'y:' in line and scanning:
        y = float(line.split(' ')[1])
    elif 'z' in line and scanning:
        scanning = False
        z = float(line.split(' ')[1])
        #print("position: ", x, y, z, '\r\n')
        # print(cmd)
        cmd = "core-pos 4 %f %f %f" % (base_x + x, base_y - y, z)
        if os.system(cmd) != 0:
            single_node = False
        elif not single_node:
            cmd = "core-pos 1 %f %f %f" % (base_x + x, base_y - y, z)
            if os.system(cmd) != 0:
                print("No second node running, only updating one node position")
                single_node = True
        last_update = time.time()
