import pandas as pd
from itertools import product
import sys
import json

"""
syntax: python3 testcasegen.py <input.json> <output.xlsx>
"""

INPUT_SET = dict()

def join_path(path, name):
    return '.'.join((path, name)).lstrip('.')

def convert_model_to_list(root, path):
    if isinstance(root, list):
        for item in root:
            if 'children' in item.keys():
                convert_model_to_list(item['children'], join_path(path, item['name']))
            else:
                if path not in INPUT_SET:
                    INPUT_SET[path] = list()
                INPUT_SET[path].append(item['name'])


input_model_path = sys.argv[1]
input_model = json.load(open(input_model_path, 'r'))
output_file = sys.argv[2]

convert_model_to_list(input_model['children'], '')

pd.DataFrame(list(product(*list(INPUT_SET.values()))), columns=[*list(INPUT_SET.keys())]).to_excel(output_file, 'Test Case')