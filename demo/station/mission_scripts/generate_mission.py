#!/usr/bin/python3

import subprocess

subprocess.run(['REMOTE_CORE=http://demo_core_1:50051 position_dump -> /home/test/position_dump.txt'], shell=True)

f = open("/home/test/position_dump.txt", "r")
elements = f.readlines()
for element in elements:
    exec(element)
f.close
