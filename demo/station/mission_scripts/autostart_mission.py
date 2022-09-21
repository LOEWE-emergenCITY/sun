#!/usr/bin/python3

import asyncio
from time import sleep
from generate_mission import elements
from appJar import gui

from mavsdk import System
import mavsdk.mission_raw 


async def run():
    app = gui()
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
    
    app.infoBox('Survey Start', 'Ready to start the survey?', parent=None)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting survey")
    await drone.mission.start_mission()

    print("waiting for survey to be finished...")

    async for mission_progress in drone.mission_raw.mission_progress():
        print(f"Survey progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")
        if mission_progress.current==mission_progress.total-1:
            await drone.action.hold()
            break

    #while not(await drone.mission.is_mission_finished()):
    #    sleep(5)
        
    print(f"survey finished, found {len(elements)-2} users")

    mission_import_data = await drone.mission_raw.import_qgroundcontrol_mission("/home/test/missions/mission12.plan")
    print(f"{len(mission_import_data.mission_items)} mission items imported")
    await drone.mission_raw.upload_mission(mission_import_data.mission_items)
    
    print("Mission uploaded")

    app.infoBox('Mission Start', 'Ready to start the mission?', parent=None)

    #print("-- Arming")
    #await drone.action.arm()

    print("-- Starting mission")
    await drone.mission_raw.start_mission()

    async for mission_progress in drone.mission_raw.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}"
              f"users served")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
