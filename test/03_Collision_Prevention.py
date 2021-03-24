#!/usr/bin/env python3

import os
import lgsvl
import time
import sys
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')

logging.debug('Initializing Simulation Variables...')
MAX_EGO_SPEED = mph_to_mps(65)
logging.info(MAX_EGO_SPEED)
SPEED_VARIANCE = 10  # Simple Physics does not return an accurate value
MAX_POV_SPEED = mph_to_mps(65)
MAX_POV_ROTATION = 5  # deg/s
TIME_LIMIT = 30
TIME_DELAY = 5
MAX_FOLLOWING_DISTANCE = 50  # Apollo 3.5 is very cautious

logging.debug('Initializing Simulator...')
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

logging.debug('Initializing Map...')
if sim.current_scene == "SunnyvaleLoop":
# if sim.current_scene == "CubeTown":
# if sim.current_scene == "SingleLaneRoad":
# if sim.current_scene == "SanFrancisco":
    sim.reset()
else:
    sim.load("SunnyvaleLoop")
    # sim.load("CubeTown")
    # sim.load("SingleLaneRoad")
    # sim.load("SanFrancisco")
spawns = sim.get_spawn()
sim.set_time_of_day(12)
# spawn EGO in the 2nd to right lane
logging.debug('Initializing EGO Car...')
egoState = lgsvl.AgentState()
egoState.transform = spawns[0]
# egoState.transform.rotation.y = 180
ego = sim.add_agent("Apollo Modular", lgsvl.AgentType.EGO, egoState)
ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)

logging.debug('Initializing NPC Car...')
POVState = lgsvl.AgentState()
POVState.transform = spawns[0]
# POVState.transform.position.z -= 50
POVState.transform.position.x -= 50
# POVState.transform.rotation.y = 180
POV = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)
# POVState2 = lgsvl.AgentState()
# POVState2.transform = sim.map_point_on_lane(lgsvl.Vector(egoX - 300, egoY, egoZ - 30))
# POV2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState2)


ego.on_collision(on_collision)
POV.on_collision(on_collision)
# # POV2.on_collision(on_collision)

try:
    t0 = time.time()
    sim.run(TIME_DELAY)  # The EGO should start moving first
    POV.follow_closest_lane(True, MAX_POV_SPEED, False)
    # POV2.follow_closest_lane(True, MAX_POV_SPEED, False)

    while True:
        # sim.run(10)
        sim.run(0.5)

        egoCurrentState = ego.state
        if egoCurrentState.speed > MAX_EGO_SPEED + SPEED_VARIANCE:
            raise TestException("Ego speed exceeded limit, {} > {} m/s".format(egoCurrentState.speed, MAX_EGO_SPEED + SPEED_VARIANCE))

        POVCurrentState = POV.state
        if POVCurrentState.speed > MAX_POV_SPEED + SPEED_VARIANCE:
            raise TestException("POV speed exceeded limit, {} > {} m/s".format(POVCurrentState.speed, MAX_POV_SPEED + SPEED_VARIANCE))
        if POVCurrentState.angular_velocity.y > MAX_POV_ROTATION:
            raise TestException("POV angular rotation exceeded limit, {} > {} deg/s".format(POVCurrentState.angular_velocity, MAX_POV_ROTATION))
        logging.info('EGO Car speed: ' + str(mps_to_mph(egoCurrentState.speed)) + 'MPH')
        logging.info('NPC Car speed: ' + str(mps_to_mph(POVCurrentState.speed)) + 'MPH')
        # logging.info('NPC Car speed: ' + str(mps_to_mph(POV2.state.speed)) + 'MPH')
        logging.info('Distance Between Cars: ' + str(separation(egoCurrentState.position, POVCurrentState.position)))
        # if separation(POVCurrentState.position, lgsvl.Vector(1.8, 0, 125)) < 5:
        #     break

        if time.time() - t0 > TIME_LIMIT:
            break
except TestException as e:
    logging.error("FAILED: " + repr(e))
    exit()