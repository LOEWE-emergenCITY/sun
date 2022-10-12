#!/usr/bin/python3
import json
import subprocess

def get_mission():
    subprocess.run(['REMOTE_CORE=http://demo_core_1:50051 position_dump -> /home/test/position_dump.txt'], shell=True)
    f = open("/home/test/position_dump.txt", "r")
    elements = f.readlines()
    for element in elements:
        exec(element)
    f.close
    #solve tsp
    #solve.tsp(positions, home)
    #transform local to global
    #save as .plan file in json format
    mission = {
    "fileType": "Plan",
    "geoFence": {
    "circles": [],
    "polygons": [],
    "version": 2
    },
    "groundStation": "QGroundControl",
    "mission": {
    "cruiseSpeed": 15,
    "firmwareType": 12,
    "hoverSpeed": 15,
    "items": [
      {
        "AMSLAltAboveTerrain": None,
        "Altitude": 50,
        "AltitudeMode": 1,
        "autoContinue": True,
        "command": 22,
        "doJumpId": 1,
        "frame": 3,
        "params": [
          15,
          0,
          0,
          None,
          49.860541,
          8.676634,
          50
        ],
        "type": "SimpleItem"
      }
      ],
    "plannedHomePosition": [
      49.860541,
      8.676634,
      181
    ],
    "vehicleType": 2,
    "version": 2
    },
    "rallyPoints": {
    "points": [],
    "version": 2
    },
    "version": 1
    }
    with open('/home/test/missions/mission13.plan', 'w') as f:
        json.dump(mission, f)
    return elements