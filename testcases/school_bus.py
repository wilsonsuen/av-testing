import sys
import os
from robot import rebot
from robot.api import TestSuite
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.testdata.school_bus import TESTDATA, EGO_DATA, SCHOOL_BUS_DATA

if __name__ == "__main__":
    main_suite = TestSuite('School Bus Scenario')
    main_suite.resource.imports.library('lib/simulation.py')

    for testdata in TESTDATA:
        lane = testdata['school bus position']
        status = testdata['school bus status']
        npc = [{
            'npc': 'SchoolBus',
            'Starting Point': SCHOOL_BUS_DATA[lane]['Starting Point'],
            'waypoints': SCHOOL_BUS_DATA[lane]['waypoints'] if status.lower() == 'moving' else\
                            SCHOOL_BUS_DATA[lane]['waypoints'][:1]
        }]
        school_bus_test = main_suite.tests.create(f'Test encounter school bus {status} on {lane}')
        school_bus_test.setup.config(name='Setup Scenario', args=["Straight2LaneOpposingPedestrianCrosswalk", EGO_DATA, npc])
        school_bus_test.body.create_keyword('Start Simulation')
        school_bus_test.teardown.config(name='Close Simulation')

    main_suite.run(output='output.xml')
    rebot('output.xml')