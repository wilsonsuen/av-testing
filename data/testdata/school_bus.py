# This is a test data file for school bus test cases.
# Data prepared using svl simulator visual editor feature.

TESTDATA = [
    {'ego speed': '10MPH', 'school bus status': 'Loading', 'school bus position': 'Backward lane'},
    # {'ego speed': '15MPH', 'school bus status': 'Loading', 'school bus position': 'Backward lane'},
    # {'ego speed': '25MPH', 'school bus status': 'Loading', 'school bus position': 'Backward lane'},
    {'ego speed': '10MPH', 'school bus status': 'Loading', 'school bus position': 'Forward lane'},
    # {'ego speed': '15MPH', 'school bus status': 'Loading', 'school bus position': 'Forward lane'},
    # {'ego speed': '25MPH', 'school bus status': 'Loading', 'school bus position': 'Forward lane'},
    {'ego speed': '10MPH', 'school bus status': 'Moving', 'school bus position': 'Backward lane'},
    # {'ego speed': '15MPH', 'school bus status': 'Moving', 'school bus position': 'Backward lane'},
    # {'ego speed': '25MPH', 'school bus status': 'Moving', 'school bus position': 'Backward lane'},
    {'ego speed': '10MPH', 'school bus status': 'Moving', 'school bus position': 'Forward lane'},
    # {'ego speed': '15MPH', 'school bus status': 'Moving', 'school bus position': 'Forward lane'},
    # {'ego speed': '25MPH', 'school bus status': 'Moving', 'school bus position': 'Forward lane'},
    {'ego speed': '10MPH', 'school bus status': 'Stop signal', 'school bus position': 'Backward lane'},
    # {'ego speed': '15MPH', 'school bus status': 'Stop signal', 'school bus position': 'Backward lane'},
    # {'ego speed': '25MPH', 'school bus status': 'Stop signal', 'school bus position': 'Backward lane'},
    {'ego speed': '10MPH', 'school bus status': 'Stop signal', 'school bus position': 'Forward lane'},
    # {'ego speed': '15MPH', 'school bus status': 'Stop signal', 'school bus position': 'Forward lane'},
    # {'ego speed': '25MPH', 'school bus status': 'Stop signal', 'school bus position': 'Forward lane'},
]

EGO_DATA = {
    'model': 'Lincoln2017MKZ_LGSVL',
    'Starting Point': {
        'spawns': 0,
        'forward': 10
        # "position": {
        #     "x": 2.57176804542542,
        #     "y": 3.93298626173412E-16,
        #     "z": 29.0876178741455
        # },
        # "rotation": {
        #     "x": 0,
        #     "y": 0.247698739171028,
        #     "z": 0
        # }
    },
    "Destination Point": {
        'forward': 100
        # "position": {
        #     "x": 2.71655941009521,
        #     "y": 3.93298626173412E-16,
        #     "z": 39.0612144470215
        # },
    }
}


SCHOOL_BUS_POSITION = {
    'Forward lane': {
        'Starting Point': {
            'forward': 20
            # "position": {
            #     "x": 2.57176804542542,
            #     "y": 3.93298626173412E-16,
            #     "z": 29.0876178741455
            # }
        },
        'waypoints': [
            {
                'forward': 40,
                # "position": { # Stop or loading only need first waypoint
                # "x": -1.39759063720703,
                # "y": -3.41121555441225E-16,
                # "z": -3.40314102172852
                # },
                "speed": 20
            },
            {
                'forward': 40,
                # "position": {
                # "x": -1.3415595293045,
                # "y": -3.8393038883722E-16,
                # "z": -49.1853523254395
                # }, 
                "speed": 20,
            }
        ]
    },
    'Backward lane': {
        'Starting Point': {
            'forward': 100,
            'right': -4,
            'opposite': True,
            # "position": {
            #     "x": -1.43843305110931,
            #     "y": -5.46772949402893E-16,
            #     "z": 29.9723320007324
            # }
        },
        'waypoints': [ # Stop or loading only need first waypoint
            {
                'forward': 40,
                # 'forward': -40,
                # "position": {
                # "x": -1.39759063720703,
                # "y": -3.41121555441225E-16,
                # "z": -3.40314102172852
                # },
                "speed": 20,
            },
            {
                'forward': 40,
                # 'forward': -40,
                # "position": {
                # "x": -1.3415595293045,
                # "y": -3.8393038883722E-16,
                # "z": -49.1853523254395
                # },
                "speed": 20,
            }
        ]
    }
}

SCHOOL_BUS_FORWARD_MOV = {
    "npc": 'SchoolBus',
}