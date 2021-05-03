#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
# Editor : Ha Duong
# Date : Apr 30, 2021
# Class: SJSU Spring 2021 CMPE 187 Sec 1


# LGSVL__SIMULATOR_HOST is the IP of the computer running the simulator
# LGSVL__AUTOPILOT_0_HOST is the IP of the computer running the bridge (from the perspective of the Simulator)
# If the simulator and bridge are running on the same computer, then the default values will work.
# Otherwise the variables must be set for in order to connect to the simulator and the bridge to receive data.
# LGSVL__SIMULATOR_PORT and LGSVL__AUTOPILOT_0_HOST need to be set if non-default ports will be used

import os
import lgsvl
import time
import sys
from environs import Env
env = Env()
SIMULATOR_HOST = os.environ.get("LGSVL__SIMULATOR_HOST", "127.0.0.1")
SIMULATOR_PORT = int(os.environ.get("LGSVL__SIMULATOR_PORT", 8181))
BRIDGE_HOST = os.environ.get("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.environ.get("LGSVL__AUTOPILOT_0_PORT", 9090))

scene_name = env.str("LGSVL__MAP", lgsvl.wise.DefaultAssets.map_sanfrancisco)

sim = lgsvl.Simulator(SIMULATOR_HOST, SIMULATOR_PORT)
if sim.current_scene == scene_name:
    sim.reset()
else:
    sim.load(scene_name, seed=0)

# spawn EGO
egoState = lgsvl.AgentState()
# Spawn point found in Unity Editor
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-189.83805847168, 10.2076635360718, 507.875854492188))
ego = sim.add_agent(os.environ.get("LGSVL__VEHICLE_0", "09510748-1f41-484e-9495-7d17129a62e3"), lgsvl.AgentType.EGO, egoState)
ego.connect_bridge(BRIDGE_HOST, BRIDGE_PORT)

right = lgsvl.utils.transform_to_right(egoState.transform) # Unit vector in the right direction of the EGO
forward = lgsvl.utils.transform_to_forward(egoState.transform) # Unit vector in the forward direction of the EGO

# spawn Hatchback
npcState = lgsvl.AgentState()
npcState.transform = egoState.transform
# npcState.transform.position = egoState.position - 3.6 * right # NPC is 3.6m to the left of the EGO
npcState.transform.position = lgsvl.Vector(-193.786315917969, 10.2076635360718, 509.739959716797)
npc = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npcState)

# spawn SUV
npc1State = lgsvl.AgentState()
# npc1State.transform = egoState.transform
npc1State.transform.position = lgsvl.Vector(-189.865310668945, 10.2076635360718, 525.102966308594)
npc1 = sim.add_agent("SUV", lgsvl.AgentType.NPC, npc1State)

# spawn BoxTruck
npc2State = lgsvl.AgentState()
npc2State.transform.position = lgsvl.Vector(-197.826690673828, 10.2076635360718, 595.357543945313)
npc2State.transform.rotation = lgsvl.Vector(3.81084123546316e-6, 180.000122070313, 0)
npc2 = sim.add_agent("BoxTruck", lgsvl.AgentType.NPC, npc2State)

# spawn Sedan
npc3State = lgsvl.AgentState()
# npc3State.transform = egoState.transform
npc3State.transform.position = lgsvl.Vector(-197.755325317383, 10.2076587677002,538.560363769531)
npc3State.transform.rotation = lgsvl.Vector(-4.01043944293633e-5, 179.928344726563, 1.59027735929476e-15)
npc3 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npc3State)


# spawn Hatchback
npc4State = lgsvl.AgentState()
npc4State.transform.position = lgsvl.Vector(-170.091552734375, 10.2076644897461,571.559387207031)
npc4State.transform.rotation = lgsvl.Vector(0, 274.830627441406, 0)
npc4 = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npc4State)

# spawn Jeep
npc5State = lgsvl.AgentState()
npc5State.transform.position = lgsvl.Vector(-222.030670166016, 10.2076635360718, 574.939147949219)
npc5State.transform.rotation = lgsvl.Vector(0,133.443252563477, 0)
npc5 = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npc5State)

# spawn SUV
npc6State = lgsvl.AgentState()
npc6State.transform.position = lgsvl.Vector(-140.0,  10.2076635360718, 557.074035644531)
npc6State.transform.rotation = lgsvl.Vector(0, 274.830627441406, 0)
npc6 = sim.add_agent("SUV", lgsvl.AgentType.NPC, npc6State)

# spawn Pamela
pesState = lgsvl.AgentState()
pesState.transform.position = lgsvl.Vector(-184.667572021484, 10.2076635360718, 548.065246582031)
pes = sim.add_agent("Pamela", lgsvl.AgentType.PEDESTRIAN, pesState)

# spawn Howard
pes1State = lgsvl.AgentState()
pes1State.transform.position = lgsvl.Vector(-172.484161376953, 10.2076635360718, 572.757690429688)
pes1 = sim.add_agent("Howard", lgsvl.AgentType.PEDESTRIAN, pes1State)

# spawn EntrepreneurFemale
pes2State = lgsvl.AgentState()
pes2State.transform.position = lgsvl.Vector(-179.342620849609, 10.207667350769, 557.752258300781)
pes2 = sim.add_agent("EntrepreneurFemale", lgsvl.AgentType.PEDESTRIAN, pes2State)

# spawn TrafficCone
state = lgsvl.ObjectState()
state.transform.position = lgsvl.Vector(-151.0,  10.2076635360718, 557.074035644531)
state.transform.rotation = lgsvl.Vector(0,0,0)
o = sim.controllable_add("TrafficCone", state)

# spawn TrafficCone
statet = lgsvl.ObjectState()
statet.transform.position = lgsvl.Vector(-150.665863037109,  11.0, 559.0)
t = sim.controllable_add("TrafficCone", statet)


# spawn TrafficCone
statecone = lgsvl.ObjectState()
statecone.transform.position = lgsvl.Vector(-150.665863037109,  11.0, 557.916259765625)
cone = sim.controllable_add("TrafficCone", statecone)


# This function will be called if a collision occurs
def on_collision(agent1, agent2, contact):
    raise Exception("{} collided with {}".format(agent1, agent2))

ego.on_collision(on_collision)
npc.on_collision(on_collision)
npc1.on_collision(on_collision)
npc2.on_collision(on_collision)
npc3.on_collision(on_collision)
npc4.on_collision(on_collision)
npc5.on_collision(on_collision)
pes.on_collision(on_collision)
pes1.on_collision(on_collision)


controlReceived = False

# This function will be called when the Simulator receives the first message on the topic defined in the CheckControlSensor configuration
def on_control_received(agent, kind, context):
    global controlReceived
    # There can be multiple custom callbacks defined, this checks for the appropriate kind
    if kind == "checkControl":
        # Stops the Simulator running, this will only interrupt the first sim.run(30) call
        sim.stop()
        controlReceived = True

ego.on_custom(on_control_received)

# Run Simulator for at most 30 seconds for the AD stack to to initialize
sim.run(100)

# If a Control message was not received, then the AD stack is not ready and the scenario should not continue
if not controlReceived:
    raise Exception("AD stack is not ready after 30 seconds")
    sys.exit()

# Way poins for npc2
Npc2Waypoints = []
Npc2Waypoints.append(lgsvl.DriveWaypoint(npc2State.transform.position, 8, npc2State.transform.rotation))
Npc2Waypoints.append(lgsvl.DriveWaypoint(lgsvl.Vector(-197.76432800293, 10.2076635360718, 425.153717041016), 0, npc2State.transform.rotation))

# Way poins for pes
waypoints = []
waypoints.append(lgsvl.WalkWaypoint(position=pesState.position, idle=0, trigger_distance=35))
waypoints.append(lgsvl.WalkWaypoint(position=lgsvl.Vector(-200.902099609375, 10.2076635360718, 548.155029296875), idle=0))
pes.follow(waypoints)

# Way poins for pes1
waypoints1 = []
waypoints1.append(lgsvl.WalkWaypoint(position=pes1State.position, idle=0, trigger_distance=40))
waypoints1.append(lgsvl.WalkWaypoint(position=lgsvl.Vector(-174.428558349609, 10.297043800354, 553.592590332031), idle=0))
pes1.follow(waypoints1)


# NPC will follow the HD map at a max speed of 15 m/s (33 mph) and will not change lanes automatically
# The speed limit of the road is 20m/s so the EGO should drive faster than the NPC
npc.follow_closest_lane(follow=True, max_speed=8, isLaneChange=False)
npc1.follow_closest_lane(follow=True, max_speed=18, isLaneChange=False)

# Uncomment to let other npcs driving, but the traffic light will not work
# npc2.follow(Npc2Waypoints)
# npc3.follow_closest_lane(follow=True, max_speed=8, isLaneChange=False)
# npc4.follow_closest_lane(follow=True, max_speed=15, isLaneChange=False)
# npc5.follow_closest_lane(follow=True, max_speed=8, isLaneChange=False)

# t0 is the time when the Simulation started
t0 = time.time()

# This will keep track of if the NPC has already changed lanes
npcChangedLanes = False

# The Simulation will pause every 0.5 seconds to check 2 conditions
while True:
    sim.run(0.5)

    # If the NPC has not already changed lanes then the distance between the NPC and EGO is calculated
    if not npcChangedLanes:
        egoCurrentState = ego.state
        npcCurrentState = npc.state

        separationDistance = (egoCurrentState.position - npcCurrentState.position).magnitude()

        # If the EGO and NPC are within 15m, then NPC will change lanes to the right (in front of the EGO)
        if separationDistance <= 15:
            npc.change_lane(False)
            npcChangedLanes = True
            
    # Simulation will be limited to running for 30 seconds total
    if time.time() - t0 > 96: 
        break
