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

    testcase_paths = glob.glob('data/testdata/03_parking/*.json')
    testcase_paths.sort()

    for testcase_path in testcase_paths:
        with open(testcase_path) as f:
            testdata = json.load(f)
        school_bus_test = main_suite.tests.create(testdata['testcase']['name'])
        school_bus_test.setup.config(name='Setup Scenario', args=[testcase_path])
        school_bus_test.body.create_keyword('Start Simulation')
        school_bus_test.teardown.config(name='Test Case Teardown')

    main_suite.run(output='results/03_parking/output.xml', loglevel="INFO")
    rebot('results/03_parking/output.xml',
          log="results/03_parking/log.html",
          report="results/03_parking/report.html")