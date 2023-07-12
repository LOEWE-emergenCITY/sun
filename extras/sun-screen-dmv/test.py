import time

from nicegui import ui
import os
import numpy as np
import datetime
import urllib3
import json


path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "demo1")
formation = {}

num_UAVs = 4
num_users = 60


# from latlon
GPS_200_lat = 49.8794921
GPS_200_lon = 8.648745509123888

GPS_H = [49.87013, 49.8842]
GPS_W = [8.630035, 8.668971]
# SCREEN_W = 2800
# SCREEN_H = 1550
SCREEN_W = 2560
SCREEN_H = 1417


for i in range(num_UAVs):
    path0 = os.path.join(path, f"drone_{i + 1}.csv")
    formation[i] = np.loadtxt(path0, delimiter=",")

formation_size = np.size(formation[0], 0)
for j in range(formation_size // 2):
    points = {"points": []}
    for i in range(num_UAVs):
        node, x, y = i, (formation[i][j + 120][0] - 200), (formation[i][j + 120][1] - 200)

        # TEST
        x, y = 1069.9256500804913 - 200, 863.7636014837772 - 200

        # x = SCREEN_W - x
        # y = SCREEN_H - y
        gps_lat = GPS_200_lat - y / 1000 / 111.32
        gps_lon = GPS_200_lon + x / 1000 / (40075 * np.cos(gps_lat) / 360)
        # gps_lat = GPS_200_lat
        # gps_lon = GPS_200_lon

        # TEST
        # gps_lat = 49.87876455
        # gps_lon = 8.648745509123888

        # x = np.clip(x, 0, SCREEN_W)
        # y = np.clip(y, 0, SCREEN_H)
        # gps = map_screen_to_gps(int(x), int(y)).split(",")
        point = {}
        point["id"] = node
        # point["lat"] = gps[0]
        # point["lon"] = gps[1]
        point["lat"] = gps_lat
        point["lon"] = gps_lon
        points["points"].append(point)
    try:
        resp = urllib3.PoolManager().urlopen(
            "POST",
            "http://10.193.0.86:14100/citymovie/json",
            body=json.dumps(points),
            headers={"Content-Type": "application/json"},
            timeout=urllib3.Timeout(connect=1.0, read=2.0),
        )
        print(resp.read())
    except Exception as e:
        print(e)

    time.sleep(1)