# SUN - Simulated UAV Network

## Architecture

```
                           ______  ___  __  ____    __
                          / __/ / / / |/ / / __/__ / /___ _____
                         _\ \/ /_/ /    / _\ \/ -_) __/ // / _ \
                        /___/\____/_/|_/ /___/\__/\__/\_,_/ .__/
                                                         /_/

           ┏━━━━━━━━━━━━━━━━━━┓                           ┏━━━━━━━━━━━━━━━━┓
           ┃  sun_station_1   ┃                           ┃  sun_uav_1     ┃
           ┃                  ┃                           ┃                ┃
           ┃  QGroundControl  ┃─ ─ ┐                 ┌ ─ ─┃  PX4 + Gazebo  ┃
           ┃                  ┃                           ┃                ┃
           ┃  vnc             ┃    │                 │    ┃                ┃
           ┗━━━━━━━━━━━━━━━━━━┛                           ┗━━━━━━━━━━━━━━━━┛
                     │             │                 │              │
                     │          ┏━━━─━─━━━━━━━━━━━━━─━━━━━┓         │
                     │          ┃  sun_core_1             ┃         │
                     │          ┃                         ┃         │
                     │          ┃  core-network emulator  ┃         │
                     │          ┃                         ┃         │
                     │          ┃  vnc / ssh              ┃         │
                     │          ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛         │
                     │                       │                      │
                     ▼                       ▼                      ▼
            ┌────────────────────────────────────────────────────────────────┐
            │                        docker host                             │
            └────────────────────────────────────────────────────────────────┘
```

## Requirements

- docker
- docker-compose
- vnc viewer

**IMPORTANT** You might need *ebtables* and *sch_netem* kernel modules loaded!

## Building demo setup

```
$ ./sun build
```

## Creating a new scenario

```
$ ./sun new myscenario
```

This will generate a new scenario under `scenarios/` with an empty `autostart.sh`, some `px4-params.txt` and an `experiment.conf` plus a few example core network topologies (default one active: `uav_direct_rj45.xml`)-

## Running a scenario setup

```
$ ./sun run scenarios/demofair22.xml
```

afterwards, connect with vnc viewer of choice to:
- groundstation at vnc://127.0.0.1:15901
- core network at vnc://127.0.0.1:15902

VNC password: `makitest`

SSH is also available on the core node at 127.0.0.1:2022
- username root
- password netsim
- alternatively: `SSHKEY` from `docker-compose.yml`

Stop the running simulation by pressing CTRL+C in the terminal.

You can access the 3 different machines also via `docker`:
- station: `docker exec -it sun_station_1 bash`
- uav: `docker exec -it sun_uav_1 bash`
- core: `docker exec -it sun_core_1 bash`

For your convenience, you can use `./sun nsh <node name>` which opens a bash on either of the three docker instances or directly on any virtual node name running within *core*.

```
$ ./sun
SUN - Simulated UAV Network

Usage: sun [command] [command options]
Commands:
  run <scenario_dir>    start simulation scenarion
  new <scenario_name>   create new scenario
  build                 build all docker images
  clear                 remove scenario results and temporary files
  nsh <node_name>       open shell for given node
  version               print version information
  help                  print this help

Nodes: uav|core|station|<coreemu virtual node name>
```

## Different network setups

There are `routed` and `direct` network setups. At the moment advanced PHY layers such as EMANE require routed scenarios. 
Any scenario file specified in `shared/experiment.conf` that begins with `uav_routed` will get the network setup of the default `uav_routed.xml` scenario. Any other scenario names will be setup as if the *station* and *uav* instances where directly within the virtual network.

