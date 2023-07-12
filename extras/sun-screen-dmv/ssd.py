#!/usr/bin/env python3
import time

from nicegui import ui
import os
import numpy as np
import datetime
import urllib3
import json


def uav1_course_generate():
    output = (
        os.popen("docker exec sun_core_1 /shared/gen_uav1_mobility.py")
        .read()
        .splitlines()
    )
    print(output)


def uav1_rth_generate():
    output = (
        os.popen("docker exec sun_core_1 /shared/rth_uav1_mobility.py")
        .read()
        .splitlines()
    )
    print(output)


def uav1_stop():
    output = (
        (
            os.popen(
                "docker exec -it sun_core_1 bash -c 'kill $(ps aux | grep automator | grep uav1 | cut -c 10-16)'"
            )
        )
        .read()
        .splitlines()
    )
    print(output)


def on_btn_uav1_stop_clicked():
    print("UAV1: stopping")
    uav1_stop()


def on_btn_uav1_clicked():
    ui.notify("UAV1: planning mission and starting")
    print("UAV1: planning mission and starting")

    uav1_rth_generate()
    uav1_course_generate()

    uav1_stop()

    output = (
        (
            os.popen(
                "docker exec -it sun_core_1 bash -c 'tmux new-session -A -s uav1 \; send -t uav1 \"nohup /shared/automator.sh /tmp/uav1_rth_mobility.pos && /shared/automator.sh /tmp/uav1_mobility.pos 1 &\" ENTER \; detach -s uav1'"
            )
        )
        .read()
        .splitlines()
    )
    print(output)


def on_btn_start_traj_clicked():
    ui.notify("Starting joint coverage and data ferrying mission")
    print("Starting joint coverage and data ferrying mission")

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "demo1")
    formation = {}

    num_UAVs = 4
    num_users = 60

    """ Draw users """
    for i in range(num_UAVs):
        path0 = os.path.join(path, f"drone_{i + 1}.csv")
        formation[i] = np.loadtxt(path0, delimiter=",")

    formation_size = np.size(formation[0], 0)
    for j in range(formation_size // 2):
        points = {"points": []}
        for i in range(num_UAVs):
            node, x, y = i, (formation[i][j + 120][0] - 200), (formation[i][j + 120][1] - 200)
            gps_lat = GPS_200_lat - y / 1000 / 111.32
            gps_lon = GPS_200_lon + x / 1000 / (40075 * np.cos(gps_lat) / 360)

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
                feed_beamer_url.value,
                body=json.dumps(points),
                headers={"Content-Type": "application/json"},
                timeout=urllib3.Timeout(connect=1.0, read=2.0),
            )
            print(resp.read())
        except Exception as e:
            print(e)
            feed_beamer.value = False
            ui.notify("Could not feed Beamer")

        """ Draw users """
        for i in range(num_users):
            path0 = os.path.join(path, f"user_{i + 1}.csv")
            formation[i] = np.loadtxt(path0, delimiter=",")

        formation_size = np.size(formation[0], 0)
        for j in range(formation_size // 2):
            points = {"points": []}
            for i in range(num_users):
                node, x, y = i, (formation[i][j + 120][0] - 200), (formation[i][j + 120][1] - 200)
                gps_lat = GPS_200_lat - y / 1000 / 111.32
                gps_lon = GPS_200_lon + x / 1000 / (40075 * np.cos(gps_lat) / 360)

                point = {}
                point["id"] = f"u{node}"
                # point["lat"] = gps[0]
                # point["lon"] = gps[1]
                point["lat"] = gps_lat
                point["lon"] = gps_lon
                points["points"].append(point)
            try:
                resp = urllib3.PoolManager().urlopen(
                    "POST",
                    feed_beamer_url.value,
                    body=json.dumps(points),
                    headers={"Content-Type": "application/json"},
                    timeout=urllib3.Timeout(connect=1.0, read=2.0),
                )
                print(resp.read())
            except Exception as e:
                print(e)
                feed_beamer.value = False
                ui.notify("Could not feed Beamer")

        time.sleep(5)


def on_btn_uav1_rth_clicked():
    ui.notify("UAV1: returning to home")
    print("UAV1: returning to home")
    uav1_rth_generate()

    uav1_stop()

    output = (
        (
            os.popen(
                "docker exec -it sun_core_1 bash -c 'tmux new-session -A -s uav1 \; send -t uav1 \"nohup /shared/automator.sh /tmp/uav1_rth_mobility.pos &\" ENTER \; detach -s uav1'"
            )
        )
        .read()
        .splitlines()
    )
    print(output)


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


def on_feed_city_demo1_changed():
    print("Feed Demo 1: " + str(feed_beamer_demo1.value))


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

# from latlon
GPS_200_lat = 49.8794921
GPS_200_lon = 8.648745509123888

GPS_H = [49.87013, 49.8842]
GPS_W = [8.630035, 8.668971]
# SCREEN_W = 2800
# SCREEN_H = 1550
SCREEN_W = 2560
SCREEN_H = 1417


def map_screen_to_gps(x, y, invertX=False, invertY=True):
    if invertX:
        x = SCREEN_W - x
    if invertY:
        y = SCREEN_H - y
    gps_lat = GPS_H[0] + (y / SCREEN_H) * (GPS_H[1] - GPS_H[0])
    gps_lon = GPS_W[0] + (x / SCREEN_W) * (GPS_W[1] - GPS_W[0])
    if (
        gps_lat < GPS_H[0]
        or gps_lat > GPS_H[1]
        or gps_lon < GPS_W[0]
        or gps_lon > GPS_W[1]
    ):
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

        if feed_beamer_demo1.value:
            raise NotImplementedError
        else:
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
            # print("feeding", json.dumps(points))
        try:
            resp = urllib3.PoolManager().urlopen(
                "POST",
                feed_beamer_url.value,
                body=json.dumps(points),
                headers={"Content-Type": "application/json"},
                timeout=urllib3.Timeout(connect=1.0, read=2.0),
            )
            print(resp.read())
        except Exception as e:
            print(e)
            feed_beamer.value = False
            ui.notify("Could not feed Beamer")

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
                ui.button("uav0: Generate Flight Plan (PX4)")
                ui.button("uav1: Generate Flight Plan", on_click=on_btn_uav1_clicked)
                ui.button("uav1: Stop", on_click=on_btn_uav1_stop_clicked)
                ui.button("uav1: RTH", on_click=on_btn_uav1_rth_clicked)
                ui.button("Start Demo 1: Joint Coverage and Data Ferrying", on_click=on_btn_start_traj_clicked)
        ui.separator()
        with ui.card():
            ui.label("Visualization: ")
            with ui.row():
                feed_beamer = ui.checkbox(
                    "Feed City Model Beamer", on_change=on_feed_city_changed
                )
                feed_beamer_url = ui.input(
                    "beamer remote", value="http://10.193.0.86:14100/citymovie/json"
                )
            with ui.row():
                feed_beamer_demo1 = ui.checkbox(
                    "UNUSED_SWITCH_FEED", on_change=on_feed_city_demo1_changed
                )
            with ui.row():
                feed_nexus = ui.checkbox(
                    "Feed NEXUS Demonstrator", on_change=on_feed_nexus_changed
                )
                feed_nexus_url = ui.input(
                    "nexus remote", value="http://localhost:8080/position"
                )

    with ui.tab_panel(two):
        view_dtn_stats = print_dtn_stats()

ui.run(title="SUN Screen - DM View")
