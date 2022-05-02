import os
import json
import time

def wait_for_mission():  ## Waits for mission instruction from JSON
    print("Waiting for Mission Instructions")
    notFound = True
    path = "/home/pi/public"
    # path = "."
    while notFound:
        paths_inside = os.listdir(path)
        print(paths_inside)
        if "mission_export.json" in paths_inside:
            notFound = False
        time.sleep(1)
    print("Mission Instructions Found")


def pull_mission_instructions():  ## Extracts mission json file from shared drive
    path = "/home/pi/public/mission_export.json"
    with open(path) as f:
        mission = json.load(f)
    return mission