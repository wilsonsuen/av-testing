import sys
import os
import glob
import json
from robot import rebot
from robot.api import TestSuite
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    
    main_suite = TestSuite('School Bus Scenario')
    main_suite.resource.imports.library('lib/simulation.py')

    testcase_paths = glob.glob('data/testdata/04_school_bus/*.json')
    testcase_paths.sort()

    for testcase_path in testcase_paths:
        with open(testcase_path) as f:
            testdata = json.load(f)
        tags = list(testdata['testcase']['context'].values()) +\
            list(testdata['testcase']['input'].values())
        school_bus_test = main_suite.tests.create(testdata['testcase']['name'], tags=tags)
        school_bus_test.setup.config(name='Setup Scenario', args=[testcase_path])
        school_bus_test.body.create_keyword('Start Simulation')
        school_bus_test.body.create_keyword('Validate Result')
        school_bus_test.teardown.config(name='Test Case Teardown')

    main_suite.run(output='results/04_school_bus/output.xml')
    rebot('results/04_school_bus/output.xml',
          log="results/04_school_bus/log.html",
          report="results/04_school_bus/report.html")

"""
rebot --tagstatcombine "8:00AMANDSunny:8AM and Sunny(C1)" --tagstatcombine "8:00AMANDCloudy:8AM and Cloudy(C2)" --tagstatcombine "8:00AMANDRainning:8AM and Rainning(C3)" --tagstatcombine "8:00AMANDFoggy:8AM and Foggy(C4)" --tagstatcombine "12:00PMANDSunny:12PM and Sunny(C5)" --tagstatcombine "12:00PMANDCloudy:12PM and Cloudy(C6)" --tagstatcombine "12:00PMANDRainning:12PM and Rainning(C7)" --tagstatcombine "12:00PMANDFoggy:12PM and Foggy(C8)" --tagstatcombine "3:00PMANDSunny:3PM and Sunny(C9)" --tagstatcombine "3:00PMANDCloudy:3PM and Cloudy(C10)" --tagstatcombine "3:00PMANDRainning:3PM and Rainning(C11)" --tagstatcombine "3:00PMANDFoggy:3PM and Foggy(C12)" --tagstatcombine "5:00PMANDSunny:5PM and Sunny(C13)" --tagstatcombine "5:00PMANDCloudy:5PM and Cloudy(C14)" --tagstatcombine "5:00PMANDRainning:5PM and Ranining(C15)" --tagstatcombine "5:00PMANDFoggy:5PM and Foggy(C16)" --tagstatcombine "7:00PMANDSunny:7PM and Sunny(C17)" --tagstatcombine "7:00PMANDCloudy:7PM and Cloudy(C18)" --tagstatcombine "7:00PMANDRainning:7PM and Rainning(C19)" --tagstatcombine "7:00PMANDFoggy:7PM and Foggy(C20)" --tagstatcombine MovingANDBackward_lane:Moving\ and\ Backward\ lane\(I12\) --tagstatcombine MovingANDForward_lane:Moving\ and\ Forward\ lane\(I9\) --tagstatcombine LoadingANDBackward_lane:Loading\ and\ Backward\ lane\(I6\) --tagstatcombine LoadingANDForward_lane:Loading\ and\ Forward\ lane\(I3\) --tagstatcombine StopANDBackward_lane:Stop\ and\ Backward\ lane\(I18\) --tagstatcombine StopANDForward_lane:Stop\ and\ Forward\ lane\(I15\) --tagstatexclude Forward_lane --tagstatexclude Backward_lane --tagstatexclude Moving --tagstatexclude Loading --tagstatexclude Stop --tagstatexclude 8\:00AM --tagstatexclude 12\:00PM --tagstatexclude 3\:00PM --tagstatexclude 5\:00PM --tagstatexclude 7\:00PM --tagstatexclude Sunny --tagstatexclude Foggy --tagstatexclude Rainning --tagstatexclude Cloudy -r combined_report.html -l combined_log.html output.xml
"""