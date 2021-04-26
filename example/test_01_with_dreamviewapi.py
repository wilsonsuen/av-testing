#!/usr/bin/env python3
import os
import lgsvl
import time
import sys
import logging
import unittest
from environs import Env
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m-%d %H:%M:%S')

class TestEncroachingVehicles(unittest.TestCase):
    sim_config = {}
    sim = None

    @classmethod
    def setUpClass(cls):
        # Initializing Simulation Variables...
        cls.env = Env()
        cls.sim_config['SIMULATOR_HOST'] = cls.env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1")
        cls.sim_config['SIMULATOR_PORT'] = cls.env.int("LGSVL__SIMULATOR_PORT", 8181)
        cls.sim_config['AUTOPILOT_0_HOST'] = cls.env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1")
        cls.sim_config['AUTOPILOT_0_PORT'] = cls.env.int("LGSVL__AUTOPILOT_0_PORT", 9090)
        cls.sim_config['EGO_MODEL'] = cls.env.str("LGSVL__VEHICLE_0", "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921")
        cls.sim_config['TIME_LIMIT'] = 25
        cls.sim_config['TIME_DELAY'] = 5
        cls.sim_config['DESTINATION_VECTOR'] = lgsvl.Vector(50.7745895385742, -0.00319480895996094, 1.72572016716003)

        # Initializing Simulator...
        cls.sim = lgsvl.Simulator(cls.sim_config['SIMULATOR_HOST'], cls.sim_config['SIMULATOR_PORT'])

        # Initializing Map...
        scene_name = cls.env.str("LGSVL__MAP", lgsvl.wise.DefaultAssets.map_singlelaneroad)
        if cls.sim.current_scene == scene_name:
            cls.sim.reset()
        else:
            cls.sim.load(scene_name)
        cls.sim.set_time_of_day(12)

    def test_encroaching_oncoming_vehicles(self):
        # Initializing EGO Car...
        egoState = lgsvl.AgentState()
        egoState.transform = self.sim.get_spawn()[0]
        ego = self.sim.add_agent(self.sim_config['EGO_MODEL'], lgsvl.AgentType.EGO, egoState)
        ego.connect_bridge(self.sim_config['AUTOPILOT_0_HOST'], self.sim_config['AUTOPILOT_0_PORT'])
        
        dv = lgsvl.dreamview.Connection(self.sim, ego, self.sim_config['AUTOPILOT_0_HOST'])
        dv.set_hd_map(self.env.str("LGSVL__AUTOPILOT_HD_MAP", 'single_lane_road'))
        dv.set_vehicle(self.env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'Lincoln2017MKZ_LGSVL'))
        try:
            modules = self.env.list("LGSVL__AUTOPILOT_0_VEHICLE_MODULES", subcast=str)
            if len(modules) == 0:
                logging.warning("LGSVL__AUTOPILOT_0_VEHICLE_MODULES is empty, using default list: {0}".format(modules))
                modules = [
                    'Localization',
                    'Transform',
                    'Routing',
                    'Prediction',
                    'Planning',
                    'Control'
                ]
        except Exception:
            modules = [
                'Localization',
                'Transform',
                'Routing',
                'Prediction',
                'Planning',
                'Control'
            ]
            logging.warning("LGSVL__AUTOPILOT_0_VEHICLE_MODULES is not set, using default list: {0}".format(modules))

        # Destination in the middle of the parking zone
        destination = self.sim_config['DESTINATION_VECTOR']
        # egoState.position + (2.75 + 4.6 + 11 + PARKING_ZONE_LENGTH / 2) * forward + 3.6 * right
        dv.setup_apollo(destination.x, destination.z, modules)

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
        