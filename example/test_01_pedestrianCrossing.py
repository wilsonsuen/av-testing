#!/usr/bin/env python3
"""
3/28 - Simulator cloud server is down, cannot run with this script.
"""

import os
import time
from environs import Env
import lgsvl
import sys
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *


env = Env()

MAX_EGO_SPEED = mph_to_mps(55)
SPEED_VARIANCE = 10  
TIME_LIMIT = 30 
TIME_DELAY = 5

LGSVL__SIMULATOR_HOST = env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1")
LGSVL__SIMULATOR_PORT = env.int("LGSVL__SIMULATOR_PORT", 8181)
LGSVL__AUTOPILOT_0_HOST = env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1")
LGSVL__AUTOPILOT_0_PORT = env.int("LGSVL__AUTOPILOT_0_PORT", 9090)

sim = lgsvl.Simulator(LGSVL__SIMULATOR_HOST, LGSVL__SIMULATOR_PORT)
scene_name = env.str("LGSVL__MAP", lgsvl.wise.DefaultAssets.map_straight1lanepedestriancrosswalk)
if sim.current_scene == scene_name:
    sim.reset()
else:
    sim.load(scene_name)

egoState = lgsvl.AgentState()
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(1, 0, 60))
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5_full_analysis), lgsvl.AgentType.EGO, egoState)
forward = lgsvl.utils.transform_to_forward(egoState.transform)
right = lgsvl.utils.transform_to_right(egoState.transform)

ego.connect_bridge(LGSVL__AUTOPILOT_0_HOST, LGSVL__AUTOPILOT_0_PORT)

dv = lgsvl.dreamview.Connection(sim, ego, LGSVL__AUTOPILOT_0_HOST)
dv.set_hd_map(env.str("LGSVL__AUTOPILOT_HD_MAP", 'Straight 1 Lane Pedestrian Crosswalk'))
dv.set_vehicle(env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'Lincoln2017MKZ'))
try:
    modules = env.list("LGSVL__AUTOPILOT_0_VEHICLE_MODULES", subcast=str)
    if len(modules) == 0:
        log.warning("LGSVL__AUTOPILOT_0_VEHICLE_MODULES is empty, using default list: {0}".format(modules))
        modules = [
            'Recorder',
            'Localization',
            'Perception',
            'Transform',
            'Routing',
            'Prediction',
            'Planning',
            'Traffic Light',
            'Control'
        ]
except Exception:
    modules = [
        'Recorder',
        'Localization',
        'Perception',
        'Transform',
        'Routing',
        'Prediction',
        'Planning',
        'Traffic Light',
        'Control'
    ]
   
destination = destination = egoState.position + 135 * forward
dv.setup_apollo(destination.x, destination.z, modules)
pedState = lgsvl.AgentState()
pedState.transform.position = lgsvl.Vector(10.3870544433594, 0.151470556855202, 6.74086332321167)
ped = sim.add_agent("Johny", lgsvl.AgentType.PEDESTRIAN, pedState)

def on_collision(agent1, agent2, contact):
    raise Exception("{} collided with {}".format(agent1, agent2))

ego.on_collision(on_collision)
ped.on_collision(on_collision)

waypoints = []
waypoints.append(lgsvl.WalkWaypoint(position=pedState.position, idle=0, trigger_distance=65))
waypoints.append(lgsvl.WalkWaypoint(position=lgsvl.Vector(-7.70540046691895, 0.151470556855202, 6.67852163314819), idle=0))
waypoints.append(lgsvl.WalkWaypoint(position=lgsvl.Vector(-7.70540046691895, 0.151470556855202, 19.0294628143311), idle=0))
ped.follow(waypoints)

endOfRoad = egoState.position + 135 * forward
try:
    t0 = time.time()
    sim.run(TIME_DELAY)  
    while True:
        sim.run(0.5)
        egoCurrentState = ego.state
        POVCurrentState = ped.state
        logging.info('Distance Between Cars: ' + str(separation(egoCurrentState.position, POVCurrentState.position)))
        logging.info('EGO Car speed: ' + str(mps_to_mph(egoCurrentState.speed)) + 'MPH')
        if separation(egoCurrentState.position, POVCurrentState.position) < 30:
            sim.assertLessEqual(egoCurrentState, egoPreviousState)
        if mps_to_mph(egoCurrentState.speed) <= 1:
                logging.info('EGO Car slow down to < 1 MPH, test complete...')
                break
        egoPreviousState = egoCurrentState
        if time.time() - t0 > sim_config['TIME_LIMIT']:
                break
