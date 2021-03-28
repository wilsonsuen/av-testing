import math

class TestException(Exception):
    pass

def mph_to_mps(mph):
    return float("{:.2f}".format(mph / 2.237))

def mps_to_mph(mps):
    return float("{:.2f}".format(mps * 2.237))

def on_collision(agent1, agent2, contact):
    raise TestException("Ego collided with {}".format(agent2))

def separation(V1, V2):
    xdiff = V1.x - V2.x
    ydiff = V1.y - V2.y
    zdiff = V1.z - V2.z
    return math.sqrt(xdiff * xdiff + ydiff * ydiff + zdiff * zdiff)
    