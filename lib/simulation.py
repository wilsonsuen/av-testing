#!/usr/bin/env python3
import os
import lgsvl
import time
import sys
import logging
import json
import matplotlib.pyplot as plt
from environs import Env
from robot.api.deco import keyword
from robot.api.logger import *
from robot.libraries.BuiltIn import BuiltIn
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *
from data.asset.svlasset import SVLAsset

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
        self.ego_state = list()
        self.npcs = list()
        self.npcs_state = list()
        self.peds = list()
        self.peds_state = list()
        self.console = True

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


    def state_point_handler(self, obj, position_data, offset_from=None, onlane=False):
        """
        forward and right in position data means it is offset from ego initial position
        """
        if 'spawns' in position_data:
            obj.transform = self.sim.get_spawn()[0]
        elif 'position' in position_data:
            if onlane:
                obj.transform = self.sim.map_point_on_lane(lgsvl.Vector(*position_data['position'].values()))
            else:
                obj.transform.position = lgsvl.Vector(*position_data['position'].values())
                if 'rotation' in position_data:
                    obj.transform.rotation = lgsvl.Vector(*position_data['rotation'].values())
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
    def setup_map_env(self, path): # could be more like trafficlight
        """ This function set up map enviroment initial stage, user can define:
        all configuration should be defined in a json file. Format follows output
        of visual editor.
        path: path to the test data json file
        """
        with open(path) as f:
            testdata = json.load(f)
        # Setup Simulator and Map
        self.testcasename = testdata['testcase']['name']
        self.testcaseid = testdata['testcase']['id']
        self.testreport_path = testdata['testcase']['reportpath']
        self.simulation_time = testdata['simulation_time']
        try: 
            os.mkdir(self.testreport_path)
        except OSError as error: 
            pass 
        

        info(f"Setup Map: {testdata['map']['name']}", also_console=self.console)
        self.set_simulator_and_map(testdata['map']['id'])
        self.reset_map()
        
        info(f"Setup Time of Day: {testdata['time']}", also_console=self.console)
        self.sim.set_time_of_day(testdata['time'])
        info(f"Setup Weather: {str(testdata['weather'])}", also_console=self.console)
        self.sim.weather = lgsvl.WeatherState(*testdata['weather'])

        ego = dict()
        npcs = list()
        peds = list()

        for agent in testdata['agents']:
            if agent['type'] == 1:
                ego = agent
            elif agent['type'] == 2:
                npcs.append(agent)
            elif agent['type'] == 3:
                peds.append(agent)
            else:
                warning(f"Unknown type: {agent['variant']}")

        # Setup EGO vehicle initial state
        info(f"Setup EGO vehicle: {ego['variant']}", also_console=self.console)
        info(f"Setup EGO Starting Point: {ego['transform']}", also_console=self.console)
        self.egoState = lgsvl.AgentState()
        self.state_point_handler(self.egoState, ego['transform'], self.egoState)
        self.ego_model = self.env.str("LGSVL__VEHICLE_0", ego['sensorsConfigurationId'])
        self.ego = self.sim.add_agent(self.ego_model, lgsvl.AgentType.EGO, self.egoState)
        self.ego.connect_bridge(self.apollo_host, self.apollo_port)
        self.ego.on_collision(on_collision)

        # Connect Simulator, EGO and Dreamview
        info(f"Connecting Dreamview: {self.apollo_host}:{self.apollo_port}", also_console=self.console)
        self.dv = lgsvl.dreamview.Connection(self.sim, self.ego, self.apollo_host)
        self.dv.set_hd_map(self.env.str("LGSVL__AUTOPILOT_HD_MAP", testdata['map']['name']))
        self.dv.set_vehicle(self.env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", ego['variant']))
        info(f"Setup EGO modules: {ego['modules']}", also_console=self.console)
        try:
            modules = self.env.list("LGSVL__AUTOPILOT_0_VEHICLE_MODULES", subcast=str)
            if len(modules) == 0:
                modules = ego['modules']
        except Exception:
            modules = ego['modules']
        egoDesState = lgsvl.AgentState()
        info(f"Setup EGO Destination Point: {ego['destinationPoint']}", also_console=self.console)
        self.state_point_handler(egoDesState, ego['destinationPoint'], self.egoState)
        self.destination = egoDesState.transform.position
        self.dv.setup_apollo(self.destination.x, self.destination.z, modules)
        
        info("Setup NPCs", also_console=self.console)
        for npc in npcs:
            info(f"Setup NPC: {npc['variant']}", also_console=self.console)
            npcState = lgsvl.AgentState()
            self.state_point_handler(npcState, npc['transform'], self.egoState)
            self.npcs.append(self.sim.add_agent(npc['variant'], lgsvl.AgentType.NPC, npcState))
            self.npcs_state.append(list())
            waypoints = list()
            for waypoint in npc['waypoints']:
                tempState = lgsvl.AgentState()
                self.state_point_handler(tempState, waypoint, npcState)
                if 'angle' in waypoint:
                    angle = lgsvl.Vector(*waypoint['angle'].values())
                else:
                    angle = npcState.transform.rotation
                waypoints.append(lgsvl.DriveWaypoint(tempState.position, waypoint['speed'], angle, idle=waypoint['waitTime']))
                if waypoints:
                    self.npcs[-1].follow(waypoints, loop=False)
            self.npcs[-1].on_collision(on_collision)

        info(f"Setup Pedestrians", also_console=self.console)
        for ped in peds:
            info(f"Setup NPC: {ped['variant']}", also_console=self.console)
            pedState = lgsvl.AgentState()
            self.state_point_handler(pedState, ped['transform'], self.egoState)
            self.peds.append(self.sim.add_agent(ped['variant'], lgsvl.AgentType.PEDESTRIAN, pedState))
            self.peds_state.append(list())
            waypoints = list()
            for waypoint in ped['waypoints']:
                tempState = lgsvl.AgentState()
                self.state_point_handler(tempState, waypoint, pedState)
                if 'angle' in waypoint:
                    angle = lgsvl.Vector(waypoint['angle'])
                else:
                    angle = lgsvl.Vector(0, 0, 0)
                waypoints.append(lgsvl.WalkWaypoint(tempState.position, waypoint['waitTime'], speed=waypoint['speed']))
                if waypoints:
                    self.peds[-1].follow(waypoints, loop=False)
            self.peds[-1].on_collision(on_collision)


    @keyword
    def start_simulation(self):
        """
        Run simulation, only collect data in this state.
        """
        t0 = time.time()
        while True:
            self.sim.run(0.5)
            self.ego_state.append(self.ego.state)
            for idx, npc in enumerate(self.npcs):
                self.npcs_state[idx].append(npc.state)
            for idx, ped in enumerate(self.peds):
                self.peds_state[idx].append(ped.state)
            if separation(self.ego.state.position, self.destination) < 3:
                info("EGO arrives destination...", also_console=True)
                break
            if time.time() - t0 > self.simulation_time: 
                break

    @keyword
    def log_simulation_data(self):
        def plot_point_data(points):
            return list(zip(*[[point.position.x, point.position.z] for point in points]))
        info(f"Generate position graph", also_console=self.console)
        plt.clf()
        plt.title("Position Mapping")
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.plot(self.ego_state[0].position.x, self.ego_state[0].position.z, 'rP', markersize=6)
        plt.plot(*plot_point_data(self.ego_state), 'ro', label='EGO', markersize=2)
        for npc_state in self.npcs_state:
            plt.plot(npc_state[0].position.x, npc_state[0].position.z, 'bP', markersize=6)
            plt.plot(*plot_point_data(npc_state), 'bo', label='NPC', markersize=2)
        for ped_state in self.peds_state:
            plt.plot(ped_state[0].position.x, ped_state[0].position.z, 'gP', markersize=6)
            plt.plot(*plot_point_data(ped_state), 'go', label='Pedestrain', markersize=2)
        plt.legend()
        plt.savefig(self.testreport_path + "/scenario_state.png")
        info(f"<img src=./{self.testcaseid}/scenario_state.png>", html=True)
        
        info(f"Generate EGO Speed graph", also_console=self.console)
        plt.clf()
        plt.title("EGO Speed Chart")
        plt.xlabel('Time (0.5s)')
        plt.ylabel('Speed (m/s)')
        egospeeds = [ego.speed for ego in self.ego_state]
        timeaxis = [i * 0.5 for i in range(1, len(self.ego_state) + 1)]
        plt.plot(timeaxis, egospeeds, 'bo', label='EGO', markersize=2)
        plt.legend()
        plt.savefig(self.testreport_path + "/ego_speed.png")
        info(f"<img src=./{self.testcaseid}/ego_speed.png>", html=True)

        info(f"Generate EGO to NPCs Distance graph", also_console=self.console)
        plt.clf()
        plt.title("EGO to NPCs Distance Chart")
        plt.xlabel('Time (0.5s)')
        plt.ylabel('Distance (meter)')
        timeaxis = [i * 0.5 for i in range(1, len(self.ego_state) + 1)]
        for npc_num, npc_state in enumerate(self.npcs_state, 1):
            distance_list = list()
            for idx, npc in enumerate(npc_state):
                distance_list.append(separation(self.ego_state[idx].position,
                                                npc.position))
            plt.plot(timeaxis, distance_list, 'bo', label=f'NPC{npc_num} to EGO', markersize=2)
        for ped_num, ped_state in enumerate(self.peds_state, 1):
            distance_list = list()
            for idx, ped in enumerate(ped_state):
                distance_list.append(separation(self.ego_state[idx].position,
                                                ped.position))
            plt.plot(timeaxis, distance_list, 'go', label=f'Pedestrian{ped_num} to EGO', markersize=2)
        plt.legend()
        plt.savefig(self.testreport_path + "/npc_to_ego.png")
        info(f"<img src=./{self.testcaseid}/npc_to_ego.png>", html=True)
    
        info(f"Saving Simulation Data", also_console=self.console)
        with open(self.testreport_path + "/agent.log", "w") as f:
            f.write("=====EGO Car State=====\n")
            f.write(str(self.ego_state) + "\n")
            for idx, npc_state in enumerate(self.npcs_state):
                f.write(f"=====NPC{idx}: {self.npcs[idx].name} State=====\n")
                f.write(str(npc_state) + "\n")
            for idx, ped_state in enumerate(self.peds_state):
                f.write(f"=====Pedestrian{idx}: {self.peds[idx].name} State=====\n")
                f.write(str(ped_state) + "\n")

    @keyword
    def validate_result(self):
        if "Loading" in self.testcasename and "Backward lane" in self.testcasename:
            raise TestException("EGO did not stop when school bus loading.")

    @keyword
    def close_simulation(self):
        self.sim.close()

    @keyword
    def test_case_teardown(self):
        BuiltIn().run_keyword("Log Simulation Data")
        BuiltIn().run_keyword("Close Simulation")

    @keyword("EGO Car driving at ${speed} and School Bus ${status} on ${lane}")
    def school_bus_case(self, speed, status, lane):
        """
        For robot example only, final product see testcases/school_bus.py
        """
        console(f'Testing - EGO Car driving at {speed} and School Bus {status} on {lane}')
        npc = [{
            'npc': 'SchoolBus',
            'Starting Point': SCHOOL_BUS_DATA[lane]['Starting Point'],
            'waypoints': SCHOOL_BUS_DATA[lane]['waypoints'] if status.lower() == 'moving' else\
                         SCHOOL_BUS_DATA[lane]['waypoints'][:1]
        }]
        self.setup_map_env("Straight2LaneOpposingPedestrianCrosswalk",
                           EGO_DATA,
                           npcs=npc)
        self.start_simulation()
        self.sim.close()


simulation = Simulation