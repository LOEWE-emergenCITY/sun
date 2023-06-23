#!/usr/bin/env python3

from copy import deepcopy
import json
import time
import random
import socket

SEND_INTERVAL = 30


def nextValue(config, node):
    nVal = deepcopy(config)
    nVal["timestamp"] = int(time.time())
    # randomize sine wave pattern on pressure base
    nVal["payload"]["pressure"] = config["payload"]["pressure"] + 2.5 * (
        0.5 - random.random()
    )
    nVal["payload"]["id"] = f"urn:ngsi:Tank:{node}_T"
    return nVal


if __name__ == "__main__":
    # load defaults from json file
    with open("watersim.json") as f:
        config = json.load(f)

    node = socket.gethostname()
    print(config)
    print(nextValue(config, node))
