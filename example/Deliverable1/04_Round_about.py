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
TIME_LIMIT = 20
TIME_DELAY = 5
MAX_FOLLOWING_DISTANCE = 50  # Apollo 3.5 is very cautious
logging.debug('Initializing Simulator...')
sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

def setup_scene(npc_car):
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
    egoState.transform.position = lgsvl.Vector(59.5960998535156, -0.00319540500640869, 16.0654678344727)
    egoState.transform.rotation = lgsvl.Vector(4.0155147871701e-05, 338.194427490234, -1.70814637385774e-05)
    ego = sim.add_agent("Apollo Modular", lgsvl.AgentType.EGO, egoState)
    ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)

    # before circle
    # POVState.transform.position = lgsvl.Vector(34.3518371582031, -0.00319543480873108, 23.6870384216309)
    # POVState.transform.rotation = lgsvl.Vector(4.02882324124221e-05, 70.309326171875, -1.75741770362947e-05)

    # On inner circle
    # POVState.transform.position = lgsvl.Vector(51.7912139892578, -0.00319540500640869, 25.2517871856689)
    # POVState.transform.rotation = lgsvl.Vector(4.02167934225872e-05, 79.0492553710938, -1.74573979165871e-05)

    logging.debug('Initializing NPC Car...')
    POVState = lgsvl.AgentState()
    POVState.transform.position = lgsvl.Vector(52.5292892456055, -0.00319519639015198, 22.3683300018311)
    POVState.transform.rotation = lgsvl.Vector(4.04969869123306e-05, 74.5680236816406, -1.7186937839142e-05)
    POV = sim.add_agent(npc_car, lgsvl.AgentType.NPC, POVState)

    ego.on_collision(on_collision)
    POV.on_collision(on_collision)

def run_scene():
    try:
        t0 = time.time()
        sim.run(TIME_DELAY)  # The EGO should start moving first
        POV.follow_closest_lane(True, MAX_POV_SPEED, False)

        while True:
            sim.run(0.5)

            egoCurrentState = ego.state
            if egoCurrentState.speed > MAX_EGO_SPEED + SPEED_VARIANCE:
                raise TestException("Ego speed exceeded limit, {} > {} m/s".format(egoCurrentState.speed, MAX_EGO_SPEED + SPEED_VARIANCE))

            POVCurrentState = POV.state
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


npc_car_types = ["Sedan", "SUV", "Jeep", "Hatchback", "SchoolBus", "BoxTruck"]

for car in npc_car_types:
    setup_scene(car)
    run_scene()
    sim.reset()
    time.sleep(2)
    
