import json
import sys
import csv
import importlib.util
import pandas as pd
sys.path.append(sys.argv[1])
from component import *
"""
# This is not perfect, just a POC
# Sample
# python3 tool/test_case_generator.py data/pretestdata/school_bus data/testdata/04_school_bus/
"""
def test_case_generation(pretestdatapath, outputpath):
    
    testcases = [{k: v for k, v in row.items() if k and (k.startswith('c_') or k.startswith('i_'))}
        for row in csv.DictReader(open(pretestdatapath + '/testtable.csv'), skipinitialspace=True)]
    for idx, testcase in enumerate(testcases, 1):
        tempjson = jsontemplate
        curr_testcasename = testcasename
        for k, v in testcase.items():
            curr_testcasename = curr_testcasename.replace(k, v)
        for header, component in components.items():
            tempvar = component[testcase[header]]
            if isinstance(tempvar, dict) and\
                (list(tempvar.keys())[0].startswith('i_') or list(tempvar.keys())[0].startswith('c_')):
                for k, v in tempvar.items():
                    tempjson = tempjson.replace(f'"{k}"', json.dumps(v))
            else:
                tempjson = tempjson.replace(f'"{header}"', json.dumps(tempvar))
        tempjson = tempjson.replace("testcasename", curr_testcasename)
        tempjson = tempjson.replace("testcaseid", testcaseid + str(idx).zfill(3))
        tempjson = tempjson.replace("testreportpath", testreportpath + "/" + testcaseid + str(idx).zfill(3))
        with open(outputpath + testcaseid + str(idx).zfill(3) + ".json", 'w') as f:
            f.write(tempjson)

if len(sys.argv) < 3:
    print('Syntax: python3 test_case_generator.py <test data path> <output path>')

test_case_generation(sys.argv[1], sys.argv[2])