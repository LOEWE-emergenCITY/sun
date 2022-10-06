#!/usr/bin/python3

def get_mission():
    f = open("/home/test/position_dump.txt", "r")
    elements = f.readlines()
    for element in elements:
        exec(element)
    f.close
    #solve tsp
    #solve.tsp(positions, home)
    #transform local to global
    #save as .plan file in json format
    return elements
