#!/usr/bin/env python3

import subprocess
import math
import copy
import sys
import os

BLACKLIST = ["ACN"]
HOME = "HQ"
SPEED = 15
STEPS_PER_SECOND = 3


def get_positions():
    os.system("position_dump > /tmp/pos.csv")
    with open("/tmp/pos.csv", "r") as f:
        elements = f.read().splitlines()
    positions = {}
    for element in elements:
        node_name, xy = element.split("=", maxsplit=1)
        if node_name not in BLACKLIST:
            positions[node_name] = [float(coord) for coord in xy.split(",")]

    return positions


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_positions_between_waypoints(positions, start, end, speed):
    x1, y1, z1 = positions[start]
    x2, y2, z2 = positions[end]
    dist = distance(x1, y1, x2, y2)
    steps = int(dist / speed) * STEPS_PER_SECOND
    if steps == 0:
        steps = 1
    x_step = (x2 - x1) / steps
    y_step = (y2 - y1) / steps
    positions_between = []
    for i in range(steps):
        positions_between.append([x1 + x_step * i, y1 + y_step * i])
    return positions_between


positions = get_positions()
# print(positions)
path = generate_positions_between_waypoints(positions, "uav1", "HQ", SPEED)
# print(path)

print("Generating UAV1 RTH mobility file...")
# print(generate_positions_between_waypoints(positions, START, path[1], SPEED))

with open("/tmp/uav1_rth_mobility.pos", "w") as f:
    f.write(f"%%delay %f\n" % (1.0 / STEPS_PER_SECOND))

    for position in path:
        f.write(f"uav1 {position[0]} {position[1]}\n")
        f.write("-- STEP\n")
