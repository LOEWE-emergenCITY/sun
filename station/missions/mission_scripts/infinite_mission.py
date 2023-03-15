#!/usr/bin/python3

import asyncio
from time import sleep

import generate_mission
import subprocess
from mavsdk import System
import mavsdk.mission_raw


async def run():
    while True:
        drone = System()  # mavsdk_server_address="localhost", port=50051
        print("trying to connect...")
        await drone.connect(system_address="udp://:14540")

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break

        mission_import_data = await drone.mission_raw.import_qgroundcontrol_mission("/home/test/missions/citydemo_mission1.plan")
        print(f"{len(mission_import_data.mission_items)} mission items imported")
        await drone.mission_raw.upload_mission(mission_import_data.mission_items)

        print("Mission uploaded")

        print("Waiting for drone to have a global position estimate...")
        async for health in drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position estimate OK")
                break

        #app.infoBox('UAV connected', 'Ready to start the survey?', parent=None)

        print("-- Arming")
        await drone.action.arm()

        print("-- Starting mission")
        await drone.mission.start_mission()

        await mission_finished(drone)

async def mission_finished(drone):
    async for mission_progress in drone.mission_raw.mission_progress():
        print("mission progress: " f"{mission_progress.current}/{mission_progress.total}")
        if mission_progress.current == 5:
            break

    # async for mission_progress in drone.mission_raw.mission_progress():
    #     subprocess.run(['REMOTE_CORE=http://sun_core_1:50051 position_dump -> /home/test/position_dump.txt'], shell=True)
    #     f = open("/home/test/position_dump.txt", "r")
    #     elements = f.readlines()
    #     for element in elements:
    #         exec(element)
    #     f.close
    #     sleep(5)
    #     print(f"Survey progress: "
    #           f"{mission_progress.current}/6")
    #     if ACN[1] < (551) and ACN[1] > (549):
    #         await drone.action.hold()
    #         break


# async def mission_preparation():
#     drone = System()#mavsdk_server_address="localhost", port=50051
#     print("trying to connect...")
#     await drone.connect(system_address="udp://:14540")

#     print("Waiting for drone to connect...")
#     async for state in drone.core.connection_state():
#         if state.is_connected:
#             print(f"-- Connected to drone!")
#             break
#    await drone.action.hold()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
