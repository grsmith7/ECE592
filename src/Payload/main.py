from cam_check import cam_check
from communication_functions import wait_for_mission, pull_mission_instructions
import time
from mission_execution_functions import execute_mission, connect_vehicle


def main():
    ## Connect to Vehicle
    vehicle = connect_vehicle("0.0.0.0:1234")

    ## Check Camera Connection
    while not cam_check():
        time.sleep(1)
    print("Camera Check complete")

    ## Mission Download
    mission = wait_for_mission()
    mission = pull_mission_instructions()
    print("Mission Found")

    ## Execute Mission and Safety Checks
    execute_mission(mission, vehicle)
    print("Mission Completed")

    ## Complete Mission Signal
    with open("/home/pi/public/mission_completed.txt", "w+") as f:
        f.write("done")
    print("Mission Complete")


if __name__ == "__main__":
    main()
