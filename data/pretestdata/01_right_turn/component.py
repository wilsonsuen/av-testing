# Data prepared using svl simulator visual editor feature.

testcasename = "Right Turn in Market Street San Francisco"

testcaseid = "AV-1."

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
        "id": "5d272540-f689-4355-83c7-03bf11b6865f",
        "name": "San Francisco",
        "parameterType": "map"
    },
    "agents": [
        {
            "id": "73805704-1e46-4eb6-b5f9-ec2244d5951e",
            "uid": "31c0b22d-c56a-417c-afe3-78f8502a3280",
            "variant": "Lincoln2017MKZ_LGSVL",
            "modules": ["Localization","Transform","Routing","Prediction","Planning","Control"],
            "type": 1,
            "parameterType": "vehicle",
            "transform": {
                "position": {
                    "x": -189.83805847168,
                    "y": 10.2076635360718,
                    "z": 507.875854492188
                },
                "rotation": {
                    "x": -4.44081206296687E-06,
                    "y": 359.909271240234,
                    "z": 3.97569339823689E-16
                }
            },
            "sensorsConfigurationId": "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921",
            "destinationPoint": {
                "position": {
                    "x": -110.707008361816,
                    "y": 10.2076635360718,
                    "z": 556.779846191406
                },
                "rotation": {
                    "x": 3.50118972341021E-15,
                    "y": 91.3937377929688,
                    "z": -2.8784963236779E-13
                }
            }
        },
        {
            "uid": "46e4ded2-0ebd-4646-a2c5-2b82bd084924",
            "variant": "BoxTruck",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -197.826690673828,
                    "y": 10.2076644897461,
                    "z": 595.357543945313
                },
                "rotation": {
                    "x": 3.81084123546316E-06,
                    "y": 180.000122070313,
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
                "r": 0.943396210670471,
                "g": 0.943396210670471,
                "b": 0.943396210670471
            },
            "waypoints": []
        },
        {
            "uid": "b5826d2b-3a32-4ed3-a609-68f5c9567565",
            "variant": "Hatchback",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -193.786315917969,
                    "y": 10.2076635360718,
                    "z": 509.739959716797
                },
                "rotation": {
                    "x": 0,
                    "y": 0.0615139789879322,
                    "z": 0
                }
            },
            "behaviour": {
                "name": "NPCLaneFollowBehaviour",
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
                        "x": -189.865310668945,
                        "y": 10.2076644897461,
                        "z": 525.102844238281
                    },
                    "angle": {
                        "x": 0,
                        "y": 359.909484863281,
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
                        "x": -189.887802124023,
                        "y": 10.2076644897461,
                        "z": 539.341796875
                    },
                    "angle": {
                        "x": 1.1775216080423E-05,
                        "y": 358.203094482422,
                        "z": -3.81666540819753E-14
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
                        "x": -190.324325561523,
                        "y": 10.2076616287231,
                        "z": 553.256103515625
                    },
                    "angle": {
                        "x": -1.20459944810136E-05,
                        "y": 358.253723144531,
                        "z": -1.2722218874358E-14
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
                        "x": -185.828216552734,
                        "y": 10.2076635360718,
                        "z": 561.706726074219
                    },
                    "angle": {
                        "x": 0,
                        "y": 97.2416000366211,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 4,
                    "position": {
                        "x": -168.649322509766,
                        "y": 10.2076635360718,
                        "z": 559.534729003906
                    },
                    "angle": {
                        "x": 0,
                        "y": 82.910270690918,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 5,
                    "position": {
                        "x": -149.474731445313,
                        "y": 10.2076635360718,
                        "z": 561.919555664063
                    },
                    "angle": {
                        "x": 0,
                        "y": 91.2873611450195,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 6,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 6,
                    "position": {
                        "x": -48.4155883789063,
                        "y": 10.2076635360718,
                        "z": 559.648498535156
                    },
                    "angle": {
                        "x": 0,
                        "y": 91.2873611450195,
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
            "uid": "f36f6c0f-f3dd-4bf9-a218-2eb3d4afbe05",
            "variant": "Sedan",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -197.755325317383,
                    "y": 10.2076587677002,
                    "z": 538.560363769531
                },
                "rotation": {
                    "x": -4.01043944293633E-05,
                    "y": 179.928344726563,
                    "z": 1.59027735929476E-15
                }
            },
            "behaviour": {
                "name": "NPCLaneFollowBehaviour",
                "parameters": {
                    "isLaneChange": false,
                    "maxSpeed": 0
                }
            },
            "color": {
                "r": 0.619607746601105,
                "g": 0.556862771511078,
                "b": 0.462745070457459
            },
            "waypoints": [
                {
                    "ordinalNumber": 0,
                    "position": {
                        "x": -197.768646240234,
                        "y": 10.2076587677002,
                        "z": 430.437347412109
                    },
                    "angle": {
                        "x": -4.01043944293633E-05,
                        "y": 179.928344726563,
                        "z": 1.59027735929476E-15
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
            "uid": "6326cb30-ced3-4dd7-bdce-f0c3b3ca897f",
            "variant": "Hatchback",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -147.671188354492,
                    "y": 10.2076635360718,
                    "z": 557.754211425781
                },
                "rotation": {
                    "x": 0,
                    "y": 94.8513412475586,
                    "z": 0
                }
            },
            "behaviour": {
                "name": "NPCLaneFollowBehaviour",
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
            "waypoints": []
        },
        {
            "uid": "4ae27593-baac-42c4-9b39-1f6ed88a6aac",
            "variant": "Pamela",
            "type": 3,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -184.667572021484,
                    "y": 10.2076635360718,
                    "z": 548.065246582031
                },
                "rotation": {
                    "x": 0,
                    "y": 270.316925048828,
                    "z": 0
                }
            },
            "waypoints": [
                {
                    "ordinalNumber": 0,
                    "position": {
                        "x": -184.667572021484,
                        "y": 10.2076635360718,
                        "z": 548.065246582031
                    },
                    "angle": {
                        "x": 0,
                        "y": 270.316925048828,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 3,
                    "trigger_distance": 35,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 1,
                    "position": {
                        "x": -200.902099609375,
                        "y": 10.2076635360718,
                        "z": 548.155029296875
                    },
                    "angle": {
                        "x": 0,
                        "y": 270.316925048828,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 3,
                    "trigger": {
                        "effectors": []
                    }
                }
            ]
        },
        {
            "uid": "8b9b47f9-bd32-48e4-9371-e81481cb0a15",
            "variant": "Howard",
            "type": 3,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -172.484161376953,
                    "y": 10.2076635360718,
                    "z": 572.757690429688
                },
                "rotation": {
                    "x": 0,
                    "y": 184.477905273438,
                    "z": 0
                }
            },
            "waypoints": [
                {
                    "ordinalNumber": 0,
                    "position": {
                        "x": -172.484161376953,
                        "y": 10.2076635360718,
                        "z": 572.757690429688
                    },
                    "angle": {
                        "x": 0,
                        "y": 184.477905273438,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 3,
                    "trigger_distance": 35,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 1,
                    "position": {
                        "x": -174.428558349609,
                        "y": 10.297043800354,
                        "z": 553.592590332031
                    },
                    "angle": {
                        "x": 0,
                        "y": 184.477905273438,
                        "z": 0
                    },
                    "waitTime": 0,
                    "speed": 3,
                    "trigger": {
                        "effectors": []
                    }
                }
            ]
        },
        {
            "uid": "18d2d58e-61ea-409a-9471-b9a1fb4a2202",
            "variant": "Jeep",
            "type": 2,
            "parameterType": "",
            "transform": {
                "position": {
                    "x": -222.030670166016,
                    "y": 10.2076635360718,
                    "z": 574.939147949219
                },
                "rotation": {
                    "x": 0,
                    "y": 133.443252563477,
                    "z": 0
                }
            },
            "behaviour": {
                "name": "NPCLaneFollowBehaviour",
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
                        "x": -153.027694702148,
                        "y": 10.2076644897461,
                        "z": 558.208801269531
                    },
                    "angle": {
                        "x": 7.11041593604023E-06,
                        "y": 63.2694892883301,
                        "z": -2.03555501989729E-13
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
    "controllables": [
        {
            "uid": "3ae22f66-6897-4b68-8eee-7f2791708600",
            "position": {
                "x": -198.677612304688,
                "y": 10.2076616287231,
                "z": 560.433166503906
            },
            "policy": [
                {
                    "action": "state",
                    "value": "green"
                }
            ],
            "spawned": false
        },
        {
            "uid": "c50d541a-5423-4f0a-a33c-a56bebda8b7b",
            "position": {
                "x": -193.898300170898,
                "y": 10.2076635360718,
                "z": 580.096740722656
            },
            "policy": [
                {
                    "action": "state",
                    "value": "green"
                }
            ],
            "spawned": false
        },
        {
            "uid": "730f8190-7719-427d-be6a-5e025e25cfae",
            "position": {
                "x": -205.86474609375,
                "y": 10.2076635360718,
                "z": 575.5908203125
            },
            "policy": [
                {
                    "action": "state",
                    "value": "red"
                }
            ],
            "spawned": false
        },
        {
            "uid": "a5b4d216-fcdb-48a1-8d73-0a7796d82ebc",
            "position": {
                "x": -186.477355957031,
                "y": 10.2076635360718,
                "z": 566.499755859375
            },
            "policy": [
                {
                    "action": "state",
                    "value": "red"
                }
            ],
            "spawned": false
        }
    ],
    "time": 17,
    "weather": {"rain": 0.0, "fog": 0, "wetness": 0, "cloudiness": 0.8, "damage": 0},
    "simulation_time": 50,
    "output": { "at_destination": true }
}"""
