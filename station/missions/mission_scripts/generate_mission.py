#!/usr/bin/python3
import subprocess
import json
import math
import numpy as np


def get_mission():

    home_global = (49.860541, 8.676634, 30)  # eHUB Koordinaten Lat Lon Alt
    waypoints_local = []

    subprocess.run(
        ['REMOTE_CORE=http://sun_core_1:50051 position_dump -> /home/test/position_dump.txt'], shell=True)
    mission = {
        'fileType': 'Plan',
        'geoFence':
        {'circles': [],
         'polygons': [],
         'version': 2},
        'groundStation': 'QGroundControl',
        'mission':
        {'cruiseSpeed': 15,
         'firmwareType': 12,
         'hoverSpeed': 15,
         'items': [],
         'plannedHomePosition': home_global,
         'vehicleType': 2,
         'version': 2},
        'rallyPoints':
        {'points': [],
         'version': 2},
        'version': 1
    }

    mission['mission']['items'] = [{
        'AMSLAltAboveTerrain': None,
        'Altitude': 30,
        'AltitudeMode': 1,
        'autoContinue': True,
        'command': 22,
        'doJumpId': 1,
        'frame': 3,
        'params': (15, 0, 0, None, home_global[0], home_global[1], home_global[2]),
        'type': 'SimpleItem'
    }]

    with open("/home/test/position_dump.txt", "r") as f:
        elements = f.read().splitlines()
    for element in elements:
        waypoints_local.append(eval(element.split('=')[1]))

    #waypoints_local = np.array([p1,p2,p3,p4,p5,p6,p7,p8,p9])
    # print(waypoints_local)

    ## PX4 can only handle global (WGS84) coordinates. Therefore we have to transform them.##
    # calculate distances from home location to waypoints
    # last point in position_dump is home_local
    home_local = np.array(waypoints_local[-1])
    home_local[1] = home_local[1]*-1

    # (only valid for small area)
    # new_latitude  = latitude  + (dy / r_earth) * (180 / pi);
    # new_longitude = longitude + (dx / r_earth) * (180 / pi) / cos(latitude * pi/180);

    coef = np.array([1, 1/math.cos(home_global[0]*math.pi/180)]
                    )*((180/math.pi)/6378000)
    #coef=((1 / r_earth) * (180 / pi), (1 / r_earth) * (180 / pi) / cos(latitude * pi/180))

    # core cs is upside down therefore y=>-y
    waypoints_local = np.array(waypoints_local)
    waypoints_local[:, 1] = waypoints_local[:, 1]*-1
    # calculate global coordinates of waypoints from distance to global home location
    waypoints_local = waypoints_local-home_local
    # x=longitude, y=latitude therefore flip array
    waypoints_global = np.array(
        [home_global[0], home_global[1]])+np.fliplr(waypoints_local[:, :2])*coef
    # (new lat, new lon)=(lat, lon)+(dy,dx)*coef
    # print(waypoints_global)

    waypoints_global.tolist()
    for waypoint in waypoints_global:
        mission['mission']['items'].append({
            'AMSLAltAboveTerrain': None,
            'Altitude': 30,
            'AltitudeMode': 1,
            'autoContinue': True,
            'command': 16,
            'doJumpId': 1,
            'frame': 3,
            'params': (15, 0, 0, None, float(waypoint[0]), float(waypoint[1]), 50),
            'type': 'SimpleItem'
        })

    json.dump(mission, open('/home/test/missions/test_mission.plan',
              'w'), indent=4, sort_keys=True)

    return elements
