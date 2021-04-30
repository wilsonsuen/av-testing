*** Settings ***
Variables    data/testdata/school_bus.py
Library      lib/simulation.py

*** Test Cases ***
School Bus Encounter
    [Tags]    School Bus    Critical
    [Template]    EGO Car driving at ${speed} and School Bus ${status} on ${lane} 
    # simulation.EGO Car driving at 10MPH and School Bus Loading on Forward lane
    FOR    ${testdata}    IN    @{TESTDATA}
        ${testdata}[ego speed]    ${testdata}[school bus status]    ${testdata}[school bus position]
    END

# School Bus Encounter2
#     [Tags]    School Bus    Critical
#     # [Template]    EGO Car driving at ${speed} and School Bus ${status} on ${lane} 
#     simulation.EGO Car driving at 10MPH and School Bus Loading on Forward lane
#     # FOR    ${testdata}    IN    @{TESTDATA}
#     #     ${testdata}[ego speed]    ${testdata}[school bus status]    ${testdata}[school bus position]
#     # END