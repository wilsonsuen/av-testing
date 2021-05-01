#!/usr/bin/env python3
import os
import lgsvl
import time
import sys
import logging
from environs import Env
from robot.api.deco import keyword
from robot.api.logger import *
from robot.libraries.BuiltIn import BuiltIn
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *
from data.asset.svlasset import SVLAsset
from data.testdata.school_bus import *

class Simulation(object):
    """
    Simulation class that help initialize lgsvl simulator and dreamview 
    """
    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self, simulator_host='127.0.0.1', simulator_port=8181, apollo_host='127.0.0.1',
                 apollo_port=9090):
        self.env = Env()
        self.simulator_host = self.env.str("LGSVL__SIMULATOR_HOST", simulator_host)
        self.simulator_port = self.env.int("LGSVL__SIMULATOR_PORT", simulator_port)
        self.apollo_host = self.env.str("LGSVL__AUTOPILOT_0_HOST", apollo_host)
        self.apollo_port = self.env.int("LGSVL__AUTOPILOT_0_PORT", apollo_port)
        self.sim = None
        self.npcs = list()
        self.peds = list()
        # self.sim = lgsvl.Simulator(self.simulator_host, self.simulator_port)

    @keyword
    def set_simulator_and_map(self, map_name):
        self.sim = lgsvl.Simulator(self.simulator_host, self.simulator_port)
        self.map_name = self.env.str("LGSVL__MAP", map_name)
        self.sim.load(self.map_name)

    @keyword
    def reset_map(self):
        if self.sim.current_scene == self.map_name:
            self.sim.reset()
        else:
            self.sim.load(self.map_name)


    def state_point_handler(self, obj, position_data, offset_from=None):
        """
        forward and right in position data means it is offset from ego initial position
        """
        if 'spawns' in position_data:
            obj.transform = self.sim.get_spawn()[0]
        elif 'position' in position_data:
            obj.transform.position = lgsvl.Vector(position_data['position'])
            obj.transform.rotation = lgsvl.Vector(position_data['rotation'])
        if 'forward' in position_data or 'right' in position_data:
            forward = lgsvl.utils.transform_to_forward(offset_from.transform)
            right = lgsvl.utils.transform_to_right(offset_from.transform)
            try:
                forward_mul = position_data['forward']
            except KeyError:
                forward_mul = 0
            try:
                right_mul = position_data['right']
            except KeyError:
                right_mul = 0
            obj.transform.position = offset_from.transform.position + forward_mul * forward + right_mul * right
        if 'opposite' in position_data and position_data['opposite']:
            obj.transform.rotation = lgsvl.Vector(obj.transform.rotation.x, obj.transform.rotation.y-180, obj.transform.rotation.z)

    @keyword('Setup Scenario')
    def setup_map_env(self, sim_map, ego, npcs=[], pedestrians=[]): # could be more like trafficlight
        """ This function set up map enviroment initial stage, user can define:
        Map(sim_map) - Map id for the map in test
        EGO car(ego) - {model, starting point, destination point}
        NPC car(npcs) - [{model, starting point, waypoints, speed, etc}...] ## maybe offset from EGO
        Pedestrian(pedestrians) - [{name, starting point, waypoints, speed, etc}...]
        """
        # Setup Simulator and Map
        self.set_simulator_and_map(getattr(SVLAsset, 'map_' + sim_map.replace('_', '').lower()))
        self.reset_map()
        # Setup EGO vehicle initial state
        self.egoState = lgsvl.AgentState()
        self.state_point_handler(self.egoState, ego['Starting Point'], self.egoState)
        self.ego_model = self.env.str("LGSVL__VEHICLE_0", getattr(SVLAsset, 'ego_' + ego['model'].lower()))
        self.ego = self.sim.add_agent(self.ego_model, lgsvl.AgentType.EGO, self.egoState)
        self.ego.connect_bridge(self.apollo_host, self.apollo_port)
        self.ego.on_collision(on_collision)

        # Connect Simulator, EGO and Dreamview
        self.dv = lgsvl.dreamview.Connection(self.sim, self.ego, self.apollo_host)
        self.dv.set_hd_map(self.env.str("LGSVL__AUTOPILOT_HD_MAP", sim_map))
        self.dv.set_vehicle(self.env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", ego['model']))
        try:
            modules = self.env.list("LGSVL__AUTOPILOT_0_VEHICLE_MODULES", subcast=str)
            if len(modules) == 0:
                # logging.warning("LGSVL__AUTOPILOT_0_VEHICLE_MODULES is empty, using default list: {0}".format(modules))
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
            # logging.warning("LGSVL__AUTOPILOT_0_VEHICLE_MODULES is not set, using default list: {0}".format(modules))
        egoDesState = lgsvl.AgentState()
        self.state_point_handler(egoDesState, ego['Destination Point'], self.egoState)
        destination = egoDesState.transform.position
        self.dv.setup_apollo(destination.x, destination.z, modules)
        for npc in npcs:
            npcState = lgsvl.AgentState()
            self.state_point_handler(npcState, npc['Starting Point'], self.egoState)
            self.npcs.append(self.sim.add_agent(npc['npc'], lgsvl.AgentType.NPC, npcState))
            waypoints = list()
            for waypoint in npc['waypoints']:
                tempState = lgsvl.AgentState()
                self.state_point_handler(tempState, waypoint, npcState)
                waypoints.append(lgsvl.DriveWaypoint(tempState.position, mph_to_mps(waypoint['speed']), npcState.transform.rotation))
            self.npcs[-1].follow(waypoints, loop=False)
            self.npcs[-1].on_collision(on_collision)

    @keyword
    def start_simulation(self):
        # while True:
        self.sim.run(10)

    @keyword
    def close_simulation(self):
        self.sim.close()

    @keyword("EGO Car driving at ${speed} and School Bus ${status} on ${lane}")
    def school_bus_case(self, speed, status, lane):
        console(f'Testing - EGO Car driving at {speed} and School Bus {status} on {lane}')
        npc = [{
            'npc': 'SchoolBus',
            'Starting Point': SCHOOL_BUS_POSITION[lane]['Starting Point'],
            'waypoints': SCHOOL_BUS_POSITION[lane]['waypoints'] if status.lower() == 'moving' else\
                         SCHOOL_BUS_POSITION[lane]['waypoints'][:1]
        }]
        self.setup_map_env("Straight2LaneOpposingPedestrianCrosswalk",
                           EGO_DATA,
                           npcs=npc)
        self.start_simulation()
        self.sim.close()


simulation = Simulation