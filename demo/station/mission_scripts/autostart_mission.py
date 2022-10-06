#!/usr/bin/python3

import asyncio
from time import sleep
import generate_mission
import subprocess
from appJar import gui

from mavsdk import System
import mavsdk.mission_raw 


async def surveyrun():
    subprocess.run(['REMOTE_CORE=http://demo_core_1:50051 position_dump -> /home/test/position_dump.txt'], shell=True)

    app.openSubWindow("survey")
    app.addMeter("survprog")
    app.setMeterFill("survprog", "green")
    app.setMeter("survprog",0)
    app.setButton("start","already started")
    drone = System()#mavsdk_server_address="localhost", port=50051
    print("trying to connect...")
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    mission_import_data = await drone.mission_raw.import_qgroundcontrol_mission("/home/test/missions/survey.plan")
    print(f"{len(mission_import_data.mission_items)} mission items imported")
    await drone.mission_raw.upload_mission(mission_import_data.mission_items)
    
    print("Survey uploaded")

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break
    
    #app.infoBox('UAV connected', 'Ready to start the survey?', parent=None)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting survey")
    await drone.mission.start_mission()

    print("waiting for survey to be finished...")

    async for mission_progress in drone.mission_raw.mission_progress():
        print(f"Survey progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")
        app.setMeter("survprog",(mission_progress.current/mission_progress.total)*100)
        if mission_progress.current==mission_progress.total-1:
            await drone.action.hold()
            break

    elements = generate_mission.get_mission()

    app.showSubWindow("mission")
    app.destroySubWindow("survey")

    #TODO add container that can be opened during runtime
    app.openSubWindow("mission")
    app.addMessage("overview2", f"""survey finished, found {len(elements)-2} users""")
    #TODO add interface to trigger mission generation 
    #TODO add interface asking to download the mission in QGC
    app.addLabel("l2", "Start Mission?")
    app.addButton("start2", missionpress)


async def missionrun():
    drone = System()#mavsdk_server_address="localhost", port=50051
    print("trying to connect...")
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

        
    mission_import_data = await drone.mission_raw.import_qgroundcontrol_mission("/home/test/missions/mission12.plan")
    print(f"{len(mission_import_data.mission_items)} mission items imported")
    await drone.mission_raw.upload_mission(mission_import_data.mission_items)
    
    print("Mission uploaded")

    #app.infoBox('Mission Start', 'Ready to start the mission?', parent=None)


    print("-- Starting mission")
    await drone.mission_raw.start_mission()

    async for mission_progress in drone.mission_raw.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}"
              f"users served")

def surveypress(btn):
    asyncio.get_event_loop().run_until_complete(surveyrun())

def missionpress():
    asyncio.get_event_loop().run_until_complete(missionrun())

app = gui()
#survey window
app.startSubWindow("survey", modal=True)
app.setFont(12)
#TODO show image of disaster site, export gif from matlab 
app.addMessage("overview", """the disaster site is shown above. The area can 
be scanned to find people who want to communicate.""")
app.addLabel("l1", "Start Survey?")
app.addButton("start", surveypress)
app.stopSubWindow()

#mission window
app.startSubWindow("mission", modal=True)
app.setFont(12)
app.stopSubWindow()

app.go(startWindow ="survey")