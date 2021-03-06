# Data prepared using svl simulator visual editor feature.

testcasename = "Performing Stop at 3-way intersection with NPC and Pedestrian"

testcaseid = "AV-2."

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
                "x": -2.69433879852295,
                "y": 101.585525512695,
                "z": 43.4019012451172
            },
            "rotation": {
                "x": 69.5999984741211,
                "y": 180.599197387695,
                "z": 7.65419443382598E-08
            }
        }
    },
    "map": {
        "id": "06773677-1ce3-492f-9fe2-b3147e126e27",
        "name": "CubeTown",
        "parameterType": "map"
    },
    "agents": [
        {
            "id": "73805704-1e46-4eb6-b5f9-ec2244d5951e",
            "uid": "2d1254e4-9693-4d3b-9a15-685d7d6991c5",
            "variant": "Lincoln2017MKZ_LGSVL",
            "type": 1,
            "parameterType": "vehicle",
            "modules": ["Localization","Transform","Routing","Prediction","Planning","Control"],
            "transform": {
                "position": {
                    "x": -21.0516738891602,
                    "y": -7.15255964678363E-07,
                    "z": 50.1071472167969
                },
                "rotation": {
                    "x": -1.96169835475594E-13,
                    "y": 89.3110656738281,
                    "z": 2.42657067763482E-20
                }
            },
            "sensorsConfigurationId": "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921",
            "destinationPoint": {
                "position": {
                    "x": 22.8498687744141,
                    "y": -7.15255964678363E-07,
                    "z": 50.1025505065918
                },
                "rotation": {
                    "x": -1.38315818217286E-13,
                    "y": 90.6528396606445,
                    "z": -1.21328533881741E-20
                }
            }
        },
        {
            "uid": "87c8e43a-cbbf-4b19-bb2d-1a6c475bb3a2",
            "variant": "i_npc_type",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": 3.29834723472595,
                    "y": -7.15255964678363E-07,
                    "z": 31.7998733520508
                },
                "rotation": {
                    "x": 5.65502169536103E-08,
                    "y": 359.677947998047,
                    "z": 1.24240418694903E-17
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
                "r": 0.00240299617871642,
                "g": 0.18620178103447,
                "b": 0.50943398475647
            },
            "waypoints": [
                {
                    "ordinalNumber": 0,
                    "position": {
                        "x": 3.44696569442749,
                        "y": -7.15255964678363E-07,
                        "z": 49.3523292541504
                    },
                    "angle": {
                        "x": 0,
                        "y": 89.0451049804688,
                        "z": 0
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
                        "x": 38.4812507629395,
                        "y": -7.15255964678363E-07,
                        "z": 49.9362716674805
                    },
                    "angle": {
                        "x": 0,
                        "y": 89.0451049804688,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                }
            ]
        },
        {
            "uid": "7727a840-8c36-49e5-a2c9-d5026749aac2",
            "variant": "Bob",
            "type": 3,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": 9.24314594268799,
                    "y": -7.15255964678363E-07,
                    "z": 61.6146545410156
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                }
            },
            "waypoints": [
                {
                    "ordinalNumber": 0,
                    "position": {
                        "x": 9.24314594268799,
                        "y": -7.15255964678363E-07,
                        "z": 61.6146545410156
                    },
                    "angle": {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    },
                    "waitTime": 3,
                    "speed": 3,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 1,
                    "position": {
                        "x": 8.10000133514404,
                        "y": -7.15255964678363E-07,
                        "z": 44.900032043457
                    },
                    "angle": {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    },
                    "waitTime": 5,
                    "speed": 3,
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
