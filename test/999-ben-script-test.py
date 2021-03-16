#!/usr/bin/env python3
#
# Ben Version 1
#

from environs import Env
import lgsvl

env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), env.int("LGSVL__SIMULATOR_PORT", 8181))
if sim.current_scene == "CubeTown":
    sim.reset()
else:
    sim.load("CubeTown")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
forward = lgsvl.utils.transform_to_forward(spawns[0])
state.transform.position += 5 * forward  # 5m forwards
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", "Lexus2016RXHybrid (Autoware)"), lgsvl.AgentType.EGO, state)

#-------------------First Sim Section-----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to start driving foward")

# VehicleControl objects can only be applied to EGO vehicles
# You can set the steering (-1 ... 1), throttle and braking (0 ... 1), handbrake and reverse (bool)
c = lgsvl.VehicleControl()

c.throttle = 0.8

# a True in apply_control means the control will be continuously applied ("sticky"). False means the control will be applied for 1 frame
ego.apply_control(c, True)

# The simulator can be run for a set amount of time. time_limit is optional and if omitted or set to 0, then the simulator will run indefinitely
sim.run(time_limit=6.0)

#--------------------Second Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to start turning left")

c = lgsvl.VehicleControl()

c.braking
c.steering = -1.6

ego.apply_control(c, True)

sim.run(time_limit=2.0)

#--------------------Third Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to drive forward for 4 seconds")

c = lgsvl.VehicleControl()

c.throttle = 0.6

ego.apply_control(c, True)

sim.run(time_limit=4.0)

#--------------------Fourth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to turn left")

c = lgsvl.VehicleControl()

c.throttle = 0.3
c.steering = -0.3

ego.apply_control(c, True)

sim.run(time_limit=1.5)

#--------------------Fifth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to floor it for 3 seconds")

c = lgsvl.VehicleControl()

c.throttle = 1.0

ego.apply_control(c, True)

sim.run(time_limit=3.0)

#--------------------Sixth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to turn left")

c = lgsvl.VehicleControl()

c.throttle = 0.3
c.steering = -0.3

ego.apply_control(c, True)

sim.run(time_limit=1.7)

#--------------------Seventh Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to drive forward for 4 seconds")

c = lgsvl.VehicleControl()

c.throttle = 0.4

ego.apply_control(c, True)

sim.run(time_limit=4.0)

#--------------------Eighth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to turn left")

c = lgsvl.VehicleControl()

c.throttle = 0.3
c.steering = -0.25

ego.apply_control(c, True)

sim.run(time_limit=1.6)

#--------------------Ninth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to floor it for 3 seconds")

c = lgsvl.VehicleControl()

c.throttle = 1.0

ego.apply_control(c, True)

sim.run(time_limit=3.0)

#--------------------Tenth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to turn left")

c = lgsvl.VehicleControl()

c.throttle = 0.3
c.steering = -0.3

ego.apply_control(c, True)

sim.run(time_limit=1.7)

#--------------------Eleventh Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to drive forward")

c = lgsvl.VehicleControl()

c.throttle = 0.1

ego.apply_control(c, True)

sim.run(time_limit=1.5)

#--------------------Twelfth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to turn left")

c = lgsvl.VehicleControl()

c.throttle = 0.3
c.steering = -0.25

ego.apply_control(c, True)

sim.run(time_limit=1.7)

#--------------------Thirteenth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to drive forward")

c = lgsvl.VehicleControl()

c.braking

ego.apply_control(c, True)

sim.run(time_limit=0.5)

#--------------------Fourteenth Sim Section----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to start braking")

c = lgsvl.VehicleControl()

c.braking

ego.apply_control(c, True)

sim.run(time_limit=6.0)

#--------------------End of Sim----------------------------------

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)
