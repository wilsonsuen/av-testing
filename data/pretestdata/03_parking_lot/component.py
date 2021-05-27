# Data prepared using svl simulator visual editor feature.

testcasename = "Exiting Parking Lot encountering i_npc_type at c_time in c_weather day"

testcaseid = "AV-3."

components = {
    "c_weather": {
        "Sunny": {"rain": 0.0, "fog": 0, "wetness": 0, "cloudiness": 0, "damage": 0},
        "Rainning": {"rain": 0.8, "fog": 0, "wetness": 0, "cloudiness": 0, "damage": 0},
        "Foggy": {"rain": 0.0, "fog": 0.8, "wetness": 0, "cloudiness": 0, "damage": 0},
        "Cloudy": {"rain": 0.0, "fog": 0, "wetness": 0, "cloudiness": 0.8, "damage": 0}
    },
    "c_time": {
        "8:00AM": 8,
        "12:00PM": 12,
        "5:00PM": 17
    },
    "i_npc_type": {
        "Jeep": "Jeep",
        "SUV": "SUV",
        "Sedan": "Sedan",
        "Hatchback": "Hatchback",
        "SchoolBus": "SchoolBus",
        "BoxTruck": "BoxTruck"
    },
    "o_at_destination": {
        "True": True,
        "False": False
    }
}

jsontemplate = """{
    "version": "0.01",
    "testcase": {
        "name": "testcasename",
        "id": "testcaseid",
        "context": "contextinfo",
        "input": "inputinfo"
    },
    "vseMetadata": {
        "cameraSettings": {
            "position": {
                "x": -74.5729293823242,
                "y": 60,
                "z": -57.5616722106934
            },
            "rotation": {
                "x": 90,
                "y": 230.40007019043,
                "z": 0
            }
        }
    },
    "map": {
        "id": "2aae5d39-a11c-4516-87c4-cdc9ca784551",
        "name": "AutonomouStuff",
        "parameterType": "map"
    },
    "agents": [
        {
            "id": "73805704-1e46-4eb6-b5f9-ec2244d5951e",
            "uid": "4a998b0d-15ff-4559-8f7b-1ef34104f963",
            "variant": "Lincoln2017MKZ_LGSVL",
            "modules": ["Localization","Transform","Routing","Prediction","Planning","Control"],
            "type": 1,
            "parameterType": "vehicle",
            "transform": {
                "position": {
                    "x": 39.9554328918457,
                    "y": -2.42564034461975,
                    "z": -70.8712387084961
                },
                "rotation": {
                    "x": 0.547064065933228,
                    "y": 213.232345581055,
                    "z": -1.33408208924379E-08
                }
            },
            "sensorsConfigurationId": "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921",
            "destinationPoint": {
                "position": {
                    "x": 0.638561248779297,
                    "y": -2.7070779800415,
                    "z": -88.3734893798828
                },
                "rotation": {
                    "x": 359.357482910156,
                    "y": 257.065246582031,
                    "z": 0
                }
            }
        },
        {
            "uid": "484ca5f3-39f9-47c8-a442-804959e6aed6",
            "variant": "i_npc_type",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": 5.89918518066406,
                    "y": -2.9221408367157,
                    "z": -112.112930297852
                },
                "rotation": {
                    "x": 359.092681884766,
                    "y": 320.543518066406,
                    "z": 0
                }
            },
            "behaviour": {
                "name": "NPCWaypointBehaviour",
                "parameters": {
                    "isLaneChange": false,
                    "maxSpeed": 0
                }
            },
            "color": {
                "r": 1,
                "g": 0.442666590213776,
                "b": 0.251999914646149
            },
            "waypoints": [
                {
                    "ordinalNumber": 0,
                    "position": {
                        "x": 0.383377075195313,
                        "y": -2.86623859405518,
                        "z": -102.718910217285
                    },
                    "angle": {
                        "x": 359.516052246094,
                        "y": 347.360076904297,
                        "z": 6.6703442769267E-09
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 1,
                    "position": {
                        "x": -1.84525108337402,
                        "y": -2.7802140712738,
                        "z": -92.781120300293
                    },
                    "angle": {
                        "x": 0.134375885128975,
                        "y": 76.0216293334961,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 2,
                    "position": {
                        "x": 24.6181907653809,
                        "y": -2.84417295455933,
                        "z": -86.1936569213867
                    },
                    "angle": {
                        "x": 359.57373046875,
                        "y": 62.0760536193848,
                        "z": 2.66811639448861E-08
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 3,
                    "position": {
                        "x": 43.3689422607422,
                        "y": -2.60511302947998,
                        "z": -73.3020324707031
                    },
                    "angle": {
                        "x": 359.398071289063,
                        "y": 55.490478515625,
                        "z": -2.66818993566176E-08
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                }
            ]
        }
    ],
    "controllables": [],
    "time": "c_time",
    "weather": "c_weather",
    "simulation_time": 20,
    "output": { "at_destination": "o_at_destination" }
}"""
