import sys
import os
import glob
import json
from robot import rebot
from robot.api import TestSuite
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    
    main_suite = TestSuite('Parking Lot Scenario')
    main_suite.resource.imports.library('lib/simulation.py')

    testcase_paths = glob.glob('data/testdata/03_parking_lot/*.json')
    testcase_paths.sort()

    for testcase_path in testcase_paths[33:40]:
        with open(testcase_path) as f:
            testdata = json.load(f)
        tags = list(testdata['testcase']['context'].values()) +\
            list(testdata['testcase']['input'].values())
        school_bus_test = main_suite.tests.create(f"{testdata['testcase']['id']} - {testdata['testcase']['name']}",
                                                  tags=tags)
        school_bus_test.setup.config(name='Setup Scenario', args=[testcase_path])
        school_bus_test.body.create_keyword('Start Simulation')
        school_bus_test.body.create_keyword('Validate Result')
        school_bus_test.teardown.config(name='Test Case Teardown')

    main_suite.run(output='results/03_parking_lot/output.xml', loglevel="INFO")
    rebot('results/03_parking_lot/output.xml',
          log="results/03_parking_lot/log.html",
          report="results/03_parking_lot/report.html")