from take_picture import take_picture
from dronekit import LocationGlobalRelative, mavutil
import math
import time
from dronekit import VehicleMode, connect


def connect_vehicle(port):  ## Connecting to vehicle and verifying battery voltage
    vehicle = connect(port, wait_ready=True)
    print("Battery: %s" % vehicle.battery)
    print("Connected!")
    return vehicle


def execute_mission(mission, vehicle):
    # Load mission Data
    waypoints = list(mission.keys())
    mission_data = mission["waypoints"]
    waypoints = list(mission_data.keys())
    take_off_location = None

    # Iterate through waypoints
    for key in waypoints:
        waypoint_info = mission_data[key]
        waypoint_action = waypoint_info["action"]
        if waypoint_action == "Takeoff":
            take_off_location = (
                vehicle.location.global_relative_frame
            )  # Store location for RTL
            takeoff_altitude = waypoint_info["take_off_altitude"]
            takeoff(vehicle, takeoff_altitude)  # Take off
        elif waypoint_action == "GoTo":
            location = waypoint_info["action_coordinate"]
            gotoLocation(vehicle, location)  # Go to location
        elif waypoint_action == "TakePicture":
            heading = waypoint_info["heading"]
            pointToHeading(vehicle, heading)  # Turn To heading
            time.sleep(3)  # Pause For Stabilization
            take_picture(vehicle, int(key))  # Take a picture
        elif waypoint_action == "RTL":
            RTL(vehicle)  # RTL
            if take_off_location:
                # Wait to reach Take_off_location
                while not reached_location(
                    take_off_location, vehicle.location.global_relative_frame
                ):
                    time.sleep(1)
            else:
                time.sleep(20)
        elif waypoint_action == "Land":
            pass  # RTL handles landing
        else:  ## Error Case
            print(
                "Waypoint Action "
                + waypoint_action
                + " Invalid for Waypoint "
                + key
                + " in mission."
            )
            raise ValueError()


def takeoff(vehicle, takeoff_altitude):  ## Takes off to a certain altitude
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    # Wait for Arm
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    # Change to Guided Mode
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

    print("Moving")

    loc = LocationGlobalRelative(
        location["latitude"], location["longitude"], location["altitude"]
    )
    vehicle.simple_goto(loc)  # Send go to command

    # Wait to reach location
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
    # Change vehicle mode to RTL
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")
