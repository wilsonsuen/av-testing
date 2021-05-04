# This is a test data file for school bus test cases.
# Data prepared using svl simulator visual editor feature.

testcasename = "Encounter school bus i_schoolbus_status on i_schoolbus_direction at c_time in c_weather day"

testcaseid = "AV-4."

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
        "3:00PM": 15,
        "5:00PM": 17,
        "7:00PM": 19
    },
    "i_schoolbus_direction": {
        "Forward lane": {
            "i_schoolbus_startingpoint": {
                "forward": 20
            },
            "i_schoolbus_waypoints": [
                {
                    "ordinalNumber": 0,
                    "forward": 30,
                    "waitTime": "i_schoolbus_status",
                    "speed": 8.9399995803833,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 1,
                    "forward": 40,
                    "waitTime": 0,
                    "speed": 8.9399995803833,
                    "trigger": {
                        "effectors": []
                    }
                }
            ]
        },
        "Backward lane": {
            "i_schoolbus_startingpoint": {
                "forward": 100,
                "right": -4,
                "opposite": True
            },
            "i_schoolbus_waypoints": [
                {
                    "ordinalNumber": 0,
                    "forward": 40,
                    "waitTime": "i_schoolbus_status",
                    "speed": 8.9399995803833,
                    "trigger": {
                        "effectors": []
                    }
                },
                {
                    "ordinalNumber": 1,
                    "forward": 30,
                    "waitTime": 0,
                    "speed": 8.9399995803833,
                    "trigger": {
                        "effectors": []
                    }
                }
            ]
        }
    },
    "i_schoolbus_status": {
        "Stop": 5,
        "Moving": 0,
        "Loading": 30
    }
}

jsontemplate = """{
    "version": "0.01",
    "testcase": {
        "name": "testcasename",
        "id": "testcaseid"
    },
    "vseMetadata": {
        "cameraSettings": {
            "position": {
                "x": 6.2187967300415,
                "y": 100.09001159668,
                "z": -7.28806209564209
            },
            "rotation": {
                "x": 90,
                "y": 89.9999694824219,
                "z": 0
            }
        }
    },
    "map": {
        "id": "54d489b5-5682-49aa-80b3-0530bcf4ed10",
        "name": "Straight2LaneOpposingPedestrianCrosswalk",
        "parameterType": "map"
    },
    "agents": [
        {
            "id": "73805704-1e46-4eb6-b5f9-ec2244d5951e",
            "uid": "4a998b0d-15ff-4559-8f7b-1ef34104f963",
            "variant": "Lincoln2017MKZ_LGSVL",
            "type": 1,
            "parameterType": "vehicle",
            "modules": ["Localization","Transform","Routing","Prediction","Planning","Control"],
            "transform": {
                "spawns": 0,
                "forward": 10
            },
            "sensorsConfigurationId": "2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921",
            "destinationPoint": {
                "forward": 100
            }
        },
        {
            "uid": "ec9faacc-386a-41b4-ad4d-82534f101a83",
            "variant": "SchoolBus",
            "type": 2,
            "parameterType": "",
            "transform": "i_schoolbus_startingpoint",
            "behaviour": {
                "name": "NPCWaypointBehaviour",
                "parameters": {
                    "isLaneChange": false,
                    "maxSpeed": 0
                }
            },
            "color": {
                "r": 1,
                "g": 0.846774280071259,
                "b": 0
            },
            "waypoints": "i_schoolbus_waypoints"
        }
    ],
    "controllables": [],
    "time": "c_time",
    "weather": "c_weather"
}"""
