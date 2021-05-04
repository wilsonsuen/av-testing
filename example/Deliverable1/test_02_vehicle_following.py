#!/usr/bin/env python3

"""Filename: test_02_vehicle_following.py
   Description: Testing EGO vechile following other vehicle in a single lane road.
   Auther: Minli He
   Date: 2021-03-28
   Class: SJSU Spring 2021 CMPE 187 Sec 1
"""

import os
import lgsvl
import time
import sys
import logging
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')

class TestEncroachingVehicles(unittest.TestCase):
    # sim_config = {'EGO_MODEL': "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921",
    sim_config = {'EGO_MODEL': "Apollo Modular",
                  'TIME_LIMIT': 20,
                  'TIME_DELAY': 2,
                  'MAX_EGO_SPEED': mph_to_mps(25),
                  'MAX_POV_SPEED': mph_to_mps(15),
                  'MAX_FOLLOWING_DISTANCE': 20}
    sim = None

    @classmethod
    def setUpClass(cls):
        # Initializing Simulator...
        cls.sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

        # Initializing Map...
        if cls.sim.current_scene == "SingleLaneRoad":
            cls.sim.reset()
        else:
            cls.sim.load("SingleLaneRoad")
        cls.sim.set_time_of_day(12)

    def test_encroaching_oncoming_vehicles(self):
        # Initializing EGO Car...
        egoState = lgsvl.AgentState()
        egoState.transform = self.sim.get_spawn()[0]
        ego = self.sim.add_agent(self.sim_config['EGO_MODEL'], lgsvl.AgentType.EGO, egoState)
        ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)
        
        # Initializing NPC Car...
        POVState = lgsvl.AgentState()
        forward = lgsvl.utils.transform_to_forward(egoState.transform)
        POVState.transform = self.sim.map_point_on_lane(egoState.transform.position + 50 * forward)
        POV = self.sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)

        ego.on_collision(on_collision)
        POV.on_collision(on_collision)
        
        t0 = time.time()
        self.sim.run(self.sim_config['TIME_DELAY']) # Delay POV start by TIME_DELAY seconds
        POV.follow_closest_lane(True, self.sim_config['MAX_POV_SPEED'], False)

        while True:
            self.sim.run(0.5)
            egoCurrentState = ego.state
            POVCurrentState = POV.state
            logging.info('Distance Between Cars: ' + str(separation(egoCurrentState.position, POVCurrentState.position)))
            logging.info('EGO Car speed: ' + str(mps_to_mph(egoCurrentState.speed)) + 'MPH')
            logging.info('POV Car speed: ' + str(mps_to_mph(POVCurrentState.speed)) + 'MPH')
            self.assertGreater(separation(egoCurrentState.position, POVCurrentState.position), 
                               self.sim_config['MAX_FOLLOWING_DISTANCE'],
                               msg='EGO car is getting to close with POV car')
            if time.time() - t0 > self.sim_config['TIME_LIMIT']:
                break