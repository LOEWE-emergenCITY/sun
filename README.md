# SUN - Simulated UAV Network

## Architecture

```
                           ______  ___  __  ____    __
                          / __/ / / / |/ / / __/__ / /___ _____
                         _\ \/ /_/ /    / _\ \/ -_) __/ // / _ \
                        /___/\____/_/|_/ /___/\__/\__/\_,_/ .__/
                                                         /_/

           ┏━━━━━━━━━━━━━━━━━━┓                           ┏━━━━━━━━━━━━━━━━┓
           ┃  demo_station_1  ┃                           ┃  demo_uav_1    ┃
           ┃                  ┃                           ┃                ┃
           ┃  QGroundControl  ┃─ ─ ┐                 ┌ ─ ─┃  PX4 + Gazebo  ┃
           ┃                  ┃                           ┃                ┃
           ┃  vnc             ┃    │                 │    ┃                ┃
           ┗━━━━━━━━━━━━━━━━━━┛                           ┗━━━━━━━━━━━━━━━━┛
                     │             │                 │              │
                     │          ┏━━━─━─━━━━━━━━━━━━━─━━━━━┓         │
                     │          ┃  demo_core_1            ┃         │
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

## Building demo setup

```
$ cd demo
$ docker-compose build
```

## Running demo setup

```
$ cd demo
$ ./run_demo.sh
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
- station: `docker exec -it demo_station_1 bash`
- uav: `docker exec -it demo_uav_1 bash`
- core: `docker exec -it demo_core_1 bash`

## Different network setups

There are `routed` and `direct` network setups. At the moment advanced PHY layers such as EMANE require routed scenarios. 
Any scenario file specified in `shared/experiment.conf` that begins with `uav_routed` will get the network setup of the default `uav_routed.xml` scenario. Any other scenario names will be setup as if the *station* and *uav* instances where directly within the virtual network.

