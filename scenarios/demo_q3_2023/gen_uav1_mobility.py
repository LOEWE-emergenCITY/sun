#!/usr/bin/env python3

import subprocess
import math
import copy
import sys
import os

BLACKLIST = ["ACN"]
START = "HQ"
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


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = copy.deepcopy(graph)

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value

    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = copy.deepcopy(unvisited_nodes)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + distance(
                positions[current_min_node][0],
                positions[current_min_node][1],
                positions[neighbor][0],
                positions[neighbor][1],
            )
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        del unvisited_nodes[current_min_node]
        # unvisited_nodes.remove(current_min_node)

    # sort shortest path by value
    shortest_path_keys = dict(
        sorted(shortest_path.items(), key=lambda item: item[1], reverse=False)
    ).keys()
    return previous_nodes, shortest_path, list(shortest_path_keys)


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
# print(get_shortest_path(positions, START, "p1"))
path = dijkstra_algorithm(positions, START)[2]
path.append(START)
# print(path)

print("Generating UAV1 mobility file...")
# print(generate_positions_between_waypoints(positions, START, path[1], SPEED))

with open("/tmp/uav1_mobility.pos", "w") as f:
    f.write(f"%%delay %f\n" % (1.0 / STEPS_PER_SECOND))

    for i in range(len(path) - 1):
        positions_between = generate_positions_between_waypoints(
            positions, path[i], path[i + 1], SPEED
        )
        for position in positions_between:
            f.write(f"uav1 {position[0]} {position[1]}\n")
            f.write("-- STEP\n")
