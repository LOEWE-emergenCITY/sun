#!/usr/bin/python3

import asyncio

from mavsdk import System
import mavsdk.mission_raw


async def run():
    drone = System()  # mavsdk_server_address="localhost", port=50051
    print("trying to connect...")
    # which port????;system_address="udp://:14540"
    await drone.connect(system_address="udp://0.0.0.0:56834")
    print("connected")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
