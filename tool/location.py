#!/usr/bin/env python3

import os
import lgsvl
import time
import logging
import sys

if len(sys.argv) < 4:
    print("""Syntax: python3 location.py <map> <vehicle> <freq>\n
    Map: "BorregasAve" "CubeTown" "SingleLaneRoad" "SanFrancisco"...\n
    Vehicle: "Lincoln2017MKZ (Apollo 5.0)" "Apollo Modular"...\n
    Freq: 5 - display every 5 seconds\n
    ex: python3 location.py "BorregasAve" Apollo Modular" 5
    """)
    exit()

sim_map = sys.argv[1]
vehicle = sys.argv[2]
freq = sys.argv[3]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')

logging.info('Map you selected: ' + sim_map)
logging.info('Car you selected: ' + vehicle)
logging.info('Infomation Display every (s): ' + freq)

logging.info('Initializing Simulator...')
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

logging.info('Initializing Map...')
if sim.current_scene == sim_map:
    sim.reset()
else:
    sim.load(sim_map)
sim.set_time_of_day(12)

logging.info('Initializing EGO Car...')
egoState = lgsvl.AgentState()
spawns = sim.get_spawn()
egoState.transform = spawns[0]
ego = sim.add_agent(vehicle, lgsvl.AgentType.EGO, egoState)
ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)

while True:
    sim.run(float(freq))
    egoCurrentState = ego.state
    logging.info('=====================================================')
    logging.info('EGO Car Current Location: ' + str(egoCurrentState.transform.position))
    logging.info('EGO Car Current Direction: ' + str(egoCurrentState.transform.rotation))

