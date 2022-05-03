import json
import shutil
import os
import time


class Payload:
    ## Class to handle all communications with payload companion computer.
    def __init__(self) -> None:
        pass

    def send_mission(self, mission_json):
        ## Dump mission dictionary export to Shared drive for payload to recieve
        path = "X:/mission_export.json"
        with open(path, "w") as f:
            json.dump(mission_json, f)
            pass

    def receive_mission_data(self, pathTo):
        ## Copy all contents of the shared drive to pathTo folder
        path = "X:"
        paths_inside = os.listdir(path)
        for pathI in paths_inside:
            extPathTo = pathTo + "/" + pathI
            pathI = path + "/" + pathI
            print(os.path.isfile((pathI)))
            print(pathTo)
            if os.path.isfile((pathI)):
                shutil.copy(pathI, extPathTo)
        print("Mission Data Recieved and Copied")

    def wait_for_mission_completion(self):
        ## Wait for mission_completed.txt to show up in the shared drive folder, once appeared, exit function
        print("Waiting for Mission Completion")
        notFound = True
        path = "X:/"
        while notFound:
            paths_inside = os.listdir(path)
            if "mission_completed.txt" in paths_inside:
                notFound = False
            time.sleep(1)
        print("Mission Completed")
