import os
import lgsvl
import time
import sys
import logging
import evaluator
import unittest

class TestPassingVehicles(unittest.TestCase):

    MAX_SPEED = 30.06  
    SPEED_VARIANCE = 10 
    MAX_POV_SPEED = 18  
    TIME_LIMIT = 35
    TIME_DELAY = 2
    MAX_CAR_DISTANCE = 100 
    
    print("Passing Vehicles - ", end='')
    
    sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
    if sim.current_scene == "CubeTown":
        sim.reset()
    else:
        sim.load("CubeTown")
    
    # spawn EGO in the 2nd to right lane
    egoState = lgsvl.AgentState()
    egoState.transform = sim.get_spawn()[0]
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, egoState)
    egoX = ego.state.position.x
    egoY = ego.state.position.y
    egoZ = ego.state.position.z
    egoState.transform = sim.map_point_on_lane(lgsvl.Vector(egoX, egoY, egoZ -8.50))
    
    ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)
    
    #car front of EGO
    POVState = lgsvl.AgentState()
    POVState.transform = sim.map_point_on_lane(lgsvl.Vector(egoX, egoY +4.00, egoZ -11.50))
    POV = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)

    #car behind EGO
    POVState = lgsvl.AgentState()
    POVState.transform = sim.map_point_on_lane(lgsvl.Vector(egoX, egoY +4.00, egoZ +11.00))
    POV = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)

    #moving car
    POVState = lgsvl.AgentState()
    POVState.transform = sim.map_point_on_lane(lgsvl.Vector(egoX +5.00, egoY +4.00, egoZ -8.00))
    POV = sim.add_agent("Sedan", lgsvl.AgentType.NPC, POVState)

    def on_collision(agent1, agent2, contact):
        raise evaluator.TestException("Ego collided with {}".format(agent2))

    ego.on_collision(on_collision)
    POV.on_collision(on_collision)

    try:
        t0 = time.time()
        #sim.run(TIME_DELAY)  # The EGO should start moving first
        POV.follow_closest_lane(True, MAX_POV_SPEED, False)

        while True:
            sim.run(0.5)

            egoCurrentState = ego.state
            if egoCurrentState.speed > MAX_SPEED + SPEED_VARIANCE:
                raise evaluator.TestException("Ego speed exceeded limit, {} > {} m/s".format(egoCurrentState.speed, MAX_SPEED + SPEED_VARIANCE))

            POVCurrentState = POV.state
            if POVCurrentState.speed > MAX_POV_SPEED + SPEED_VARIANCE:
                raise evaluator.TestException("POV speed exceeded limit, {} > {} m/s".format(POVCurrentState.speed, MAX_POV_SPEED + SPEED_VARIANCE))
            if POVCurrentState.angular_velocity.y > 5:
                raise evaluator.TestException("POV angular rotation exceeded limit, {} > {} deg/s".format(POVCurrentState.angular_velocity, 5))

            if evaluator.separation(POVCurrentState.position, lgsvl.Vector(1.8, 0, 125)) < 5:
                break

            if time.time() - t0 > TIME_LIMIT:
                break
    except evaluator.TestException as e:
        print("FAILED: " + repr(e))
        exit()

    separation = evaluator.separation(egoCurrentState.position, POVCurrentState.position)
    if separation > MAX_CAR_DISTANCE:
        print("FAILED: EGO vehicle distance was not maintained, {} > {}".format(separation, MAX_CAR_DISTANCE))
    else:
        print("PASSED")
