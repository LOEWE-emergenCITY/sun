#!/usr/bin/env python3

from nicegui import ui
import os
import datetime
import urllib3
import json


def on_btn_dtn_single_clicked():
    ui.notify("Single message generated on random node")
    print("DTN Message Generator: Single Message")
    os.system("../send_single_bundle.sh")


def on_btn_dtn_bulk_clicked():
    ui.notify("New message generated on all nodes")
    print("DTN Message Generator: Bulk Messages")
    # print current working directory
    os.system("../send_bundles.sh")


def on_feed_city_changed():
    print("Feed City Model Beamer: " + str(feed_beamer.value))


def on_feed_nexus_changed():
    print("Feed NEXUS Demonstrator: " + str(feed_nexus.value))


def print_dtn_stats():
    return ui.aggrid(
        {
            "columnDefs": [
                {"headerName": "Node", "field": "node"},
                {"headerName": "Pos", "field": "pos"},
                {"headerName": "GPS", "field": "gps"},
                {"headerName": "Peers", "field": "peers"},
                {"headerName": "Bundles", "field": "bundles"},
            ],
            "rowData": [],
        }
    )


GPS_H = [49.87013, 49.8842]
GPS_W = [8.630035, 8.668971]
#SCREEN_W = 2800
#SCREEN_H = 1550
SCREEN_W = 2560
SCREEN_H = 1417


def map_screen_to_gps(x, y, invertX = False, invertY = True):
    if invertX:
        x = SCREEN_W-x
    if invertY:
        y = SCREEN_H-y
    gps_lat = GPS_H[0] + (y / SCREEN_H) * (GPS_H[1] - GPS_H[0])
    gps_lon = GPS_W[0] + (x / SCREEN_W) * (GPS_W[1] - GPS_W[0])
    if gps_lat < GPS_H[0] or gps_lat > GPS_H[1] or gps_lon < GPS_W[0] or gps_lon > GPS_W[1]:
        return "out of bounds! ", x, y

    return "%.05f,%.05f" % (gps_lat, gps_lon)


def update_stats():
    global running
    if not running:
        return

    # print("update stats")
    output = os.popen("../get_dtn_stats.py").read().splitlines()
    # print(output)
    rows = []
    for line in output:
        node, pos, peers, bundles = line.strip().split()
        rows.append(
            {
                "node": node,
                "pos": pos,
                "peers": peers,
                "bundles": bundles,
                "gps": map_screen_to_gps(
                    int(pos.split(",")[0]), int(pos.split(",")[1])
                ),
            }
        )

    if ctrl_dtn_stats.options["rowData"] != rows:
        ctrl_dtn_stats.options["rowData"] = rows
        view_dtn_stats.options["rowData"] = rows
        ctrl_dtn_stats.update()
        view_dtn_stats.update()


def watchdog():
    containers_running = int(os.popen("docker ps | grep sun_ |wc -l").read().strip())
    # print("Containers running: " + str(containers_running))
    global running
    if containers_running == 3:
        running = True
    else:
        running = False


def on_feed_timer():
    if feed_beamer.value:
        points = {"points": []}
        output = os.popen("docker exec sun_core_1 dump_xy.sh").read().splitlines()
        for line in output:
            # print(line)
            node, x, y = line.strip().split()
            gps = map_screen_to_gps(int(x), int(y)).split(",")
            point = {}
            point["id"] = node
            point["lat"] = gps[0]
            point["lon"] = gps[1]
            points["points"].append(point)
        print("feeding", json.dumps(points))
        resp = urllib3.PoolManager().urlopen(
            "POST",
            "http://10.193.0.86:14100/citymovie/json",
            body=json.dumps(points),
            headers={"Content-Type": "application/json"},
            timeout=urllib3.Timeout(connect=1.0, read=2.0),
        )        
        print(resp.read())

    if feed_nexus.value:
        pass


ui.timer(1.0, update_stats)
ui.timer(5.0, watchdog)
ui.timer(1.0, on_feed_timer)

running = False

with ui.row():
    ui.markdown("# SUN Screen - DM View")

ui.spinner("audio", size="lg", color="red").bind_visibility(globals(), "running")
label = ui.label()

with ui.tabs().classes("w-full") as tabs:
    one = ui.tab("Control")
    two = ui.tab("View")

with ui.tab_panels(tabs, value=one).classes("w-full"):
    with ui.tab_panel(one):
        global ctrl_dtn_stats
        ctrl_dtn_stats = print_dtn_stats()
        ui.separator()
        with ui.card():
            ui.label("DTN Message Generator: ")
            with ui.row():
                ui.button("Single", on_click=on_btn_dtn_single_clicked)
                ui.button("Bulk", on_click=on_btn_dtn_bulk_clicked)
        ui.separator()
        with ui.card():
            ui.label("UAV Control: ")
            with ui.row():
                ui.button("Generate Flight Plan")
        ui.separator()
        with ui.card():
            ui.label("Visualization: ")
            with ui.row():
                feed_beamer = ui.checkbox(
                    "Feed City Model Beamer", on_change=on_feed_city_changed
                )
                ui.input(
                    "beamer remote", value="http://10.193.0.86:14100/citymovie/json"
                )
            with ui.row():
                feed_nexus = ui.checkbox(
                    "Feed NEXUS Demonstrator", on_change=on_feed_nexus_changed
                )
                ui.input("nexus remote", value="http://localhost:8080/position")
    with ui.tab_panel(two):
        view_dtn_stats = print_dtn_stats()

ui.run(title="SUN Screen - DM View")
