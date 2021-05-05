import sys
import os
import glob
import json
from robot import rebot
from robot.api import TestSuite
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    
    main_suite = TestSuite('Stop Sign Scenario')
    main_suite.resource.imports.library('lib/simulation.py')

    testcase_paths = glob.glob('data/testdata/02_stop_sign/*.json')
    testcase_paths.sort()

    for testcase_path in testcase_paths:
        with open(testcase_path) as f:
            testdata = json.load(f)
        school_bus_test = main_suite.tests.create(testdata['testcase']['name'])
        school_bus_test.setup.config(name='Setup Scenario', args=[testcase_path])
        school_bus_test.body.create_keyword('Start Simulation')
        school_bus_test.body.create_keyword('Log Simulation Data')
        school_bus_test.teardown.config(name='Close Simulation')

    main_suite.run(output='results/02_stop_sign/output.xml')
    rebot('results/02_stop_sign/output.xml',
          log="results/02_stop_sign/log.html",
          report="results/02_stop_sign/report.html")
