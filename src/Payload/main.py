import json
import math
from click import pass_context
from dronekit import connect, VehicleMode
import time
import os
from take_picture import take_picture
from cam_check import cam_check
from dronekit import LocationGlobalRelative, mavutil


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


def takeoff(vehicle, takeoff_altitude):  ## Takes off to a certain altitude
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")

    print("Taking off!")
    vehicle.simple_takeoff(takeoff_altitude)  # Take off to target altitude
    print("Target Altitude: ", takeoff_altitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if (
            vehicle.location.global_relative_frame.alt >= takeoff_altitude * 0.95
        ):  ## Waits until reach close to target altitude
            print("Reached target altitude")
            break
        time.sleep(1)


def gotoLocation(vehicle, location):
    # uncomment below for sample location
    # location  = {'latitude': 35.7737254, 'longitude': -78.6658496, 'altitude': None}
    print("Moving")
    loc = LocationGlobalRelative(
        location["latitude"], location["longitude"], location["altitude"]
    )
    vehicle.simple_goto(loc)
    while not reached_location(loc, vehicle.location.global_relative_frame):
        pass
    time.sleep(5)
    print("Reached location " + str(location))
    print("Location Real: ", vehicle.location.global_relative_frame)


def reached_location(
    ref_loc, new_loc, alpha=0.0001
):  # Verifies if the UAV has reached the location
    if (abs(new_loc.lat - ref_loc.lat)) > alpha:  # Lat
        return False
    if (abs(new_loc.lon - ref_loc.lon)) > alpha:  # Long
        return False
    if (
        abs(new_loc.alt - ref_loc.alt)
    ) > alpha * 100000:  # Altitude ## Altitude is supposed to stay the relatively same
        return False
    return True


def pointToHeading(vehicle, heading):  ## Pointing to a heading (in degrees)

    msg = vehicle.message_factory.command_long_encode(
        0,
        0,  # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
        0,  # confirmation
        heading,  # param 1, yaw in degrees
        0,  # param 2, yaw speed deg/s
        1,  # param 3, direction -1 ccw, 1 cw
        0,  # param 4, relative offset 1, absolute angle 0
        0,
        0,
        0,
    )  # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
    print("Turning to: " + str(heading) + " degrees")  ## Turning
    notReached = True
    time.sleep(2)
    radiansToDegrees = 180 / math.pi
    while notReached:
        if vehicle.attitude.yaw * radiansToDegrees - heading < 1:
            notReached = False
        time.sleep(0.5)
    print("Heading Reached")


def RTL(vehicle):
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")


def execute_mission(mission, vehicle):
    waypoints = list(mission.keys())
    mission_data = mission["waypoints"]
    waypoints = list(mission_data.keys())
    take_off_location = None
    for key in waypoints:
        waypoint_info = mission_data[key]
        waypoint_action = waypoint_info["action"]
        if waypoint_action == "Takeoff":
            take_off_location = vehicle.location.global_relative_frame
            takeoff_altitude = waypoint_info["take_off_altitude"]
            takeoff(vehicle, takeoff_altitude)
        elif waypoint_action == "GoTo":
            location = waypoint_info["action_coordinate"]
            gotoLocation(vehicle, location)
        elif waypoint_action == "TakePicture":
            heading = waypoint_info["heading"]
            pointToHeading(vehicle, heading)
            time.sleep(3)  # For Stabilization
            take_picture(vehicle, int(key))
        elif waypoint_action == "RTL":
            RTL(vehicle)
            if take_off_location:
                while not reached_location(
                    take_off_location, vehicle.location.global_relative_frame
                ):
                    time.sleep(1)
            else:
                time.sleep(20)
        elif waypoint_action == "Land":
            pass
            # land(vehicle)
            # time.sleep(20)
        else:  ## Error Case
            print(
                "Waypoint Action "
                + waypoint_action
                + " Invalid for Waypoint "
                + key
                + " in mission."
            )
            raise ValueError()


def connect_vehicle(port):  ## Connecting to vehicle and verifying battery voltage
    vehicle = connect(port, wait_ready=True)
    print("Battery: %s" % vehicle.battery)
    print("Connected!")
    return vehicle


def main():
    ## Connect to Vehicle
    vehicle = connect_vehicle("0.0.0.0:1234")
    ## Safety Checks
    # ADD SAFETY CHECKLIST
    while not cam_check():
        time.sleep(1)
    print("Camera Check complete")
    print("Preflight Checks Completed")

    ## Mission Download
    mission = wait_for_mission()
    mission = pull_mission_instructions()
    print("Mission Found")

    ## Execute Mission
    execute_mission(mission, vehicle)
    print("Mission Completed")

    ## Compile and Export Mission Data
    # ADD MISSION EXPORT FUNCTION
    print("Mission Data Exported")
    with open("/home/pi/public/mission_completed.txt", "w+") as f:
        f.write("done")
    print("Mission Complete")


if __name__ == "__main__":
    main()
