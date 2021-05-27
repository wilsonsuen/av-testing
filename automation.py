import sys
import os
import glob
import json
import argparse
import logging
from pathlib import Path
from robot import rebot
from robot.api import TestSuite
from tool.test_case_generator import test_case_generation
sys.path.append(os.path.dirname(__file__))


def simulation_test(testdatapath, reportpath):
    scenario_name = os.path.split(testdatapath)[1].replace("_", " ").title()
    main_suite = TestSuite(f'{scenario_name} Scenario')
    main_suite.resource.imports.library('lib/simulation.py', args=[reportpath])
    testcase_paths = glob.glob(os.path.join(testdatapath, '*.json'))
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

    main_suite.run(output=os.path.join(reportpath, 'output.xml'))
    rebot(os.path.join(reportpath, 'output.xml'),
          log=os.path.join(reportpath, "log.html"),
          report=os.path.join(reportpath, "report.html"))

def stress_test(testdatapath, reportpath, cycle):
    scenario_name = os.path.split(testdatapath)[1].replace("_", " ").title()
    main_suite = TestSuite(f'Stress {scenario_name} Scenario - {cycle} Cycles')
    main_suite.resource.imports.library('lib/simulation.py', args=[reportpath])
    with open(testdatapath) as f:
        testdata = json.load(f)
    tags = list(testdata['testcase']['context'].values()) +\
           list(testdata['testcase']['input'].values())
    for round in range(1, cycle + 1):
        school_bus_test = main_suite.tests.create(f"{testdata['testcase']['name']} - round{str(round)}", tags=tags)
        school_bus_test.setup.config(name='Setup Scenario', args=[testdatapath, round])
        school_bus_test.body.create_keyword('Start Simulation')
        school_bus_test.body.create_keyword('Validate Result')
        school_bus_test.teardown.config(name='Test Case Teardown')

    main_suite.run(output=os.path.join(reportpath, 'output.xml'))
    rebot(os.path.join(reportpath, 'output.xml'),
          log=os.path.join(reportpath, "log.html"),
          report=os.path.join(reportpath, "report.html"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='AV-Testing Automation')
    parser.add_argument('--testcasegen', help='Test Case Generator', action='store_true')
    parser.add_argument('--pretestdata', help='Pretest data path', type=Path)
    parser.add_argument('--testcasedata', help='Test Case file output path', type=Path)
    parser.add_argument('--automation', help='Run Automation', action='store_true')
    parser.add_argument('--reportpath', help='Test Case file output path', type=Path)
    parser.add_argument('--stress', help='Stress test cycle number', type=int)
    parser.add_argument('-d', '--debug', help='Debug mode', action='store_true')
    args = parser.parse_args()

    is_command_specified = (args.automation or args.testcasegen or args.stress)

    if not is_command_specified:
        parser.print_usage()
        raise SystemExit(1)

    if args.testcasegen:
        if not (args.pretestdata and args.testcasedata):
            logging.error("Test case generator required: pretestdata and testcasedata arguments")
            raise SystemExit(1)
        else:
            if not os.path.exists(args.pretestdata):
                logging.error("Pretest data not exist")
                raise SystemExit(1)
            if not os.path.exists(args.testcasedata):
                os.makedirs(args.testcasedata)
            test_case_generation(os.path.abspath(args.pretestdata),
                                 os.path.abspath(args.testcasedata))
    elif args.automation:
        if not (args.reportpath and args.testcasedata):
            logging.error("Automation required: reportpath and testcasedata arguments")
            raise SystemExit(1)
        else:
            if glob.glob(os.path.join(args.testcasedata, '*.json')):
                if not os.path.exists(args.testcasedata):
                    logging.error("Test Data does not exist")
                    raise SystemExit(1)
                if not os.path.exists(args.reportpath):
                    os.makedirs(args.reportpath)
                simulation_test(args.testcasedata, args.reportpath)
            else:
                for eachfile in os.listdir(args.testcasedata):
                    if eachfile.startswith("__"):
                        continue
                    testdatapath = os.path.abspath(os.path.join(args.testcasedata, eachfile))
                    testreportpath = os.path.abspath(os.path.join(args.reportpath, eachfile))
                    if os.path.isdir(testdatapath):
                        if not os.path.exists(testreportpath):
                            os.makedirs(testreportpath)
                        simulation_test(testdatapath, testreportpath)
    elif args.stress:
        if not (args.reportpath and args.testcasedata):
            logging.error("Stress test required: reportpath and testcasedata arguments")
            raise SystemExit(1)
        else:
            if not str(args.testcasedata).endswith(".json"):
                logging.error("reportpath for stress test must be .json")
                raise SystemExit(1)
            if not os.path.exists(args.reportpath):
                os.makedirs(args.reportpath)
            stress_test(args.testcasedata, args.reportpath, args.stress)

"""
rebot --tagstatcombine "8:00AMANDSunny:8AM and Sunny(C1)" --tagstatcombine "8:00AMANDCloudy:8AM and Cloudy(C2)" --tagstatcombine "8:00AMANDRainning:8AM and Rainning(C3)" --tagstatcombine "8:00AMANDFoggy:8AM and Foggy(C4)" --tagstatcombine "12:00PMANDSunny:12PM and Sunny(C5)" --tagstatcombine "12:00PMANDCloudy:12PM and Cloudy(C6)" --tagstatcombine "12:00PMANDRainning:12PM and Rainning(C7)" --tagstatcombine "12:00PMANDFoggy:12PM and Foggy(C8)" --tagstatcombine "3:00PMANDSunny:3PM and Sunny(C9)" --tagstatcombine "3:00PMANDCloudy:3PM and Cloudy(C10)" --tagstatcombine "3:00PMANDRainning:3PM and Rainning(C11)" --tagstatcombine "3:00PMANDFoggy:3PM and Foggy(C12)" --tagstatcombine "5:00PMANDSunny:5PM and Sunny(C13)" --tagstatcombine "5:00PMANDCloudy:5PM and Cloudy(C14)" --tagstatcombine "5:00PMANDRainning:5PM and Ranining(C15)" --tagstatcombine "5:00PMANDFoggy:5PM and Foggy(C16)" --tagstatcombine "7:00PMANDSunny:7PM and Sunny(C17)" --tagstatcombine "7:00PMANDCloudy:7PM and Cloudy(C18)" --tagstatcombine "7:00PMANDRainning:7PM and Rainning(C19)" --tagstatcombine "7:00PMANDFoggy:7PM and Foggy(C20)" --tagstatcombine MovingANDBackward_lane:Moving\ and\ Backward\ lane\(I12\) --tagstatcombine MovingANDForward_lane:Moving\ and\ Forward\ lane\(I9\) --tagstatcombine LoadingANDBackward_lane:Loading\ and\ Backward\ lane\(I6\) --tagstatcombine LoadingANDForward_lane:Loading\ and\ Forward\ lane\(I3\) --tagstatcombine StopANDBackward_lane:Stop\ and\ Backward\ lane\(I18\) --tagstatcombine StopANDForward_lane:Stop\ and\ Forward\ lane\(I15\) --tagstatexclude Forward_lane --tagstatexclude Backward_lane --tagstatexclude Moving --tagstatexclude Loading --tagstatexclude Stop --tagstatexclude 8\:00AM --tagstatexclude 12\:00PM --tagstatexclude 3\:00PM --tagstatexclude 5\:00PM --tagstatexclude 7\:00PM --tagstatexclude Sunny --tagstatexclude Foggy --tagstatexclude Rainning --tagstatexclude Cloudy -r combined_report.html -l combined_log.html output.xml
"""