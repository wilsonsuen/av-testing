#!/usr/bin/env python3

"""Filename: test_03_encroaching_vehicle.py
   Description: Testing EGO vechile handle encroaching incoming vechicle scenario in lgsvl simulator.
   Auther: Wai Yin (Wilson) Suen
   Date: 2021-03-28
   Class: SJSU Spring 2021 CMPE 287 Sec 1
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
    sim_config = {}
    sim = None

    @classmethod
    def setUpClass(cls):
        # Initializing Simulation Variables...
        cls.sim_config['EGO_MODEL'] = "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921"
        cls.sim_config['TIME_LIMIT'] = 20
        cls.sim_config['TIME_DELAY'] = 5

        # Initializing Simulator...
        cls.sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)

        # Initializing Map...
        if cls.sim.current_scene == "BorregasAve":
            cls.sim.reset()
        else:
            cls.sim.load("BorregasAve")
        cls.sim.set_time_of_day(12)

    def test_encroaching_oncoming_vehicles(self):
        # Initializing EGO Car...
        egoState = lgsvl.AgentState()
        egoState.transform.position = lgsvl.Vector(54.9349937438965, -3.07091188430786, -34.2451934814453)
        egoState.transform.rotation = lgsvl.Vector(0.818352222442627, 100.853286743164, 2.66831463591188E-08)
        ego = self.sim.add_agent(self.sim_config['EGO_MODEL'], lgsvl.AgentType.EGO, egoState)
        ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)
        # desctiptionPoint -> position (165.119781494141, -4.55315732955933, -63.1689682006836)
        #                  -> rotation () 0.825478792190552, 104.742340087891, 0)
        
        # Initializing NPC Car...
        POVState = lgsvl.AgentState()
        POVState.transform.position = lgsvl.Vector(185.055068969727, -4.79732370376587, -64.5046615600586)
        POVState.transform.rotation = lgsvl.Vector(359.176055908203, 284.852416992188, -2.66831836626125E-08)
        POV = self.sim.add_agent("Jeep", lgsvl.AgentType.NPC, POVState)

        # Waypoints for POV
        waypoints = [
            lgsvl.DriveWaypoint(lgsvl.Vector(156.138732910156, -4.41972684860229, -56.8363418579102),
                                mph_to_mps(25), 
                                lgsvl.Vector(359.313537597656, 266.701354980469, 0)),
            lgsvl.DriveWaypoint(lgsvl.Vector(139.314392089844, -4.20983266830444, -56.378662109375),
                                mph_to_mps(20), 
                                lgsvl.Vector(359.285491943359, 271.558258056641, -2.66824997652293E-08)),
        ]

        ego.on_collision(on_collision)
        POV.on_collision(on_collision)
        
        t0 = time.time()
        self.sim.run(self.sim_config['TIME_DELAY']) # Delay POV start by TIME_DELAY seconds
        POV.follow(waypoints, loop=False)
        egoPreviousState = ego.state

        while True:
            self.sim.run(0.5)
            egoCurrentState = ego.state
            POVCurrentState = POV.state
            logging.info('Distance Between Cars: ' + str(separation(egoCurrentState.position, POVCurrentState.position)))
            logging.info('EGO Car speed: ' + str(mps_to_mph(egoCurrentState.speed)) + 'MPH')
            if separation(egoCurrentState.position, POVCurrentState.position) < 30:
                # Starts checking when distance between 2 cars is closeer than 50 meters.
                self.assertLessEqual(egoCurrentState.speed, egoPreviousState.speed)
            if mps_to_mph(egoCurrentState.speed) <= 1:
                logging.info('EGO Car slow down to < 1 MPH, test complete...')
                break
            egoPreviousState = egoCurrentState
            if time.time() - t0 > self.sim_config['TIME_LIMIT']:
                break