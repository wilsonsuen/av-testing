#!/usr/bin/env python3
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
    sim_config = {}
    sim = None

    @classmethod
    def setUpClass(cls):
        # Initializing Simulation Variables...
        cls.sim_config['EGO_MODEL'] = "Apollo Modular"
        cls.sim_config['TIME_LIMIT'] = 25
        cls.sim_config['TIME_DELAY'] = 5
        cls.sim_config['DESTINATION_VECTOR'] = lgsvl.Vector(50.7745895385742, -0.00319480895996094, 1.72572016716003)

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
        pedState = lgsvl.AgentState()
        forward = lgsvl.utils.transform_to_forward(egoState.transform)
        right = lgsvl.utils.transform_to_right(egoState.transform)
        pedState.transform.position = egoState.position + 50 * forward - 6 * right
        ped = self.sim.add_agent("Johny", lgsvl.AgentType.PEDESTRIAN, pedState)

        # Waypoints for ped
        waypoints = [
            lgsvl.DriveWaypoint(pedState.position + 7 * right,
                                mph_to_mps(3)),
            lgsvl.DriveWaypoint(pedState.position,
                                mph_to_mps(3)),
        ]

        ego.on_collision(on_collision)
        ped.on_collision(on_collision)
        
        t0 = time.time()
        self.sim.run(self.sim_config['TIME_DELAY']) # Delay ped start by TIME_DELAY seconds
        ped.follow(waypoints, loop=False)
        egoPreviousState = ego.state

        while True:
            self.sim.run(0.5)
            egoCurrentState = ego.state
            pedCurrentState = ped.state
            logging.info('EGO Car speed: ' + str(mps_to_mph(egoCurrentState.speed)) + 'MPH')
            if time.time() - t0 > self.sim_config['TIME_LIMIT']:
                break
        egoCurrentState = ego.state
        self.assertLessEqual(separation(egoCurrentState.position,
                                        self.sim_config['DESTINATION_VECTOR']),
                             1, msg="FAILED: Destination Not Reached")    
        