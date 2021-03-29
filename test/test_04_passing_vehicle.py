import os
import lgsvl
import time
import sys
import logging
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *

class TestPassingVehicles(unittest.TestCase):

    MAX_SPEED = 30.06  
    SPEED_VARIANCE = 10 
    MAX_POV_SPEED = 18  
    INITIAL_HEADWAY = 50  # spec says >30m
    TIME_LIMIT = 35
    TIME_DELAY = 0
    MAX_CAR_DISTANCE = 100
    DESTINATION_VECTOR = lgsvl.Vector(-2.25873184204102, -0.00319525599479675, -38.3513984680176)
    
    print("Passing Vehicles - ", end='')
    
    sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
    if sim.current_scene == "CubeTown":
        sim.reset()
    else:
        sim.load("CubeTown")
    
    # spawn EGO in the 2nd to right lane
    egoState = lgsvl.AgentState()
    egoState.transform = sim.get_spawn()[0]
    ego = sim.add_agent("Apollo Modular", lgsvl.AgentType.EGO, egoState)
    egoX = ego.state.position.x
    egoY = ego.state.position.y
    egoZ = ego.state.position.z
    egoState.transform = sim.map_point_on_lane(lgsvl.Vector(egoX, egoY, egoZ -8.50))
    
    ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)
    
    forward = lgsvl.utils.transform_to_forward(egoState.transform)
    right = lgsvl.utils.transform_to_right(egoState.transform)
    #car front of EGO
    POVState = lgsvl.AgentState()
    POVState.transform = sim.map_point_on_lane(egoState.transform.position + 10 * forward)
    POV1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)

    #moving car
    POVState = lgsvl.AgentState()
    POVState.transform.position = egoState.position + (4.5 + INITIAL_HEADWAY) * forward - 4.3 * right
    # POVState.transform.rotation = lgsvl.Vector(0, -180, 0)
    POV2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)

    ego.on_collision(on_collision)
    POV1.on_collision(on_collision)
    POV2.on_collision(on_collision)

    def test_passing_vehicle(self):

        t0 = time.time()
        #sim.run(TIME_DELAY)  # The EGO should start moving first
        self.POV2.follow_closest_lane(True, self.MAX_POV_SPEED, False)

        while True:
            self.sim.run(0.5)
            egoCurrentState = self.ego.state
            if egoCurrentState.speed > self.MAX_SPEED + self.SPEED_VARIANCE:
                raise TestException("Ego speed exceeded limit, {} > {} m/s".format(egoCurrentState.speed, MAX_SPEED + SPEED_VARIANCE))

            POV1CurrentState = self.POV1.state
            if POV1CurrentState.speed > self.MAX_POV_SPEED + self.SPEED_VARIANCE:
                raise TestException("POV speed exceeded limit, {} > {} m/s".format(POV1CurrentState.speed, self.MAX_POV_SPEED + self.SPEED_VARIANCE))
            if POV1CurrentState.angular_velocity.y > 5:
                raise TestException("POV angular rotation exceeded limit, {} > {} deg/s".format(POVCurrentState.angular_velocity, 5))

            if separation(POV1CurrentState.position, lgsvl.Vector(1.8, 0, 125)) < 5:
                break

            if separation(egoCurrentState.position, self.DESTINATION_VECTOR) < 1:
                print('Destination Reached')
                break
            if time.time() - t0 > self.TIME_LIMIT:
                break

        egoCurrentState = self.ego.state
        distance = separation(egoCurrentState.position, self.DESTINATION_VECTOR)
        self.assertLessEqual(distance, 1, msg="FAILED: Destination Not Reached")    
        