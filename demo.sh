#/bin/bash

python3 tool/test_case_generator.py data/pretestdata/school_bus data/testdata/04_school_bus/
echo "Generated 120 test case data files"
sleep 5
python3 testcases/school_bus.py