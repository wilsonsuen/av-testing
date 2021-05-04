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
MAX_EGO_SPEED = mph_to_mps(25)
logging.info(MAX_EGO_SPEED)
SPEED_VARIANCE = 10  # Simple Physics does not return an accurate value
MAX_POV_SPEED = mph_to_mps(25)
MAX_POV_ROTATION = 5  # deg/s
TIME_LIMIT = 30
TIME_DELAY = 5
MAX_FOLLOWING_DISTANCE = 50  # Apollo 3.5 is very cautious
logging.debug('Initializing Simulator...')
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

global POV, ego
logging.debug('Initializing Map...')
if sim.current_scene == "Shalun":
    sim.reset()
else:
    sim.load("Shalun")
spawns = sim.get_spawn()
sim.set_time_of_day(12)
# spawn EGO in the 2nd to right lane
logging.debug('Initializing EGO Car...')
egoState = lgsvl.AgentState()
egoState.transform.position = lgsvl.Vector(8.97555255889893, -0.00319534540176392, 14.4848661422729)
egoState.transform.rotation = lgsvl.Vector(4.01737852371298e-05, 69.6051635742188, -1.7305494111497e-05)
ego = sim.add_agent("Apollo Modular", lgsvl.AgentType.EGO, egoState)
ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)


logging.debug('Initializing NPC Car 1...')
POVState1 = lgsvl.AgentState()
POVState1.transform.position = lgsvl.Vector(24.6529731750488, -0.00319471955299377, 12.9393510818481)
POVState1.transform.rotation = lgsvl.Vector(3.68428554793354e-05, 69.7994155883789, 4.36133586845244e-06)
POV1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState1)


# logging.debug('Initializing NPC Car 2...')
# POVState2 = lgsvl.AgentState()
# POVState2.transform.position = lgsvl.Vector(31.1994209289551, -0.00324535369873047, 15.4232568740845)
# POVState2.transform.rotation = lgsvl.Vector(359.918273925781, 70.7255859375, -2.48695178015623e-05)
# POV2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState2)

logging.debug('Initializing NPC Car 3...')
POVState3 = lgsvl.AgentState()
POVState3.transform.position = lgsvl.Vector(35.8044548034668, -0.0031980574131012, 17.0448188781738)
POVState3.transform.rotation = lgsvl.Vector(0.00158595538232476, 69.798713684082, -1.14077583930339e-05)
POV3 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState3)


ego.on_collision(on_collision)
POV1.on_collision(on_collision)
# POV2.on_collision(on_collision)
POV3.on_collision(on_collision)

try:
    t0 = time.time()
    sim.run(TIME_DELAY)  # The EGO should start moving first
    # POV.follow_closest_lane(True, MAX_POV_SPEED, False)

    while True:
        sim.run(0.5)

        egoCurrentState = ego.state
        if egoCurrentState.speed > MAX_EGO_SPEED + SPEED_VARIANCE:
            raise TestException("Ego speed exceeded limit, {} > {} m/s".format(egoCurrentState.speed, MAX_EGO_SPEED + SPEED_VARIANCE))

        POVCurrentState = POV1.state
        # if POVCurrentState.speed > MAX_POV_SPEED + SPEED_VARIANCE:
        #     raise TestException("POV speed exceeded limit, {} > {} m/s".format(POVCurrentState.speed, MAX_POV_SPEED + SPEED_VARIANCE))
        # if POVCurrentState.angular_velocity.y > MAX_POV_ROTATION:
        #     raise TestException("POV angular rotation exceeded limit, {} > {} deg/s".format(POVCurrentState.angular_velocity, MAX_POV_ROTATION))
        logging.info('EGO Car speed: ' + str(mps_to_mph(egoCurrentState.speed)) + 'MPH')
        logging.info('NPC Car speed: ' + str(mps_to_mph(POVCurrentState.speed)) + 'MPH')
        logging.info('Distance Between Cars: ' + str(separation(egoCurrentState.position, POVCurrentState.position)))
        # if separation(POVCurrentState.position, lgsvl.Vector(1.8, 0, 125)) < 5:
        #     break

        if time.time() - t0 > TIME_LIMIT:
            break
except TestException as e:
    logging.error("FAILED: " + repr(e))
    exit()
