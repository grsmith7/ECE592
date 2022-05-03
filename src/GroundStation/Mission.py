import json

from Geolocation import Geolocation


class Mission:
    ## Object used to store mission information as a series of waypoints
    def __init__(self, waypoints) -> None:
        self.waypoints = waypoints

    def export_mission_as_dict(self):
        ## This function converts the mission object and any internal objects into a json format used by the payload.
        result = {"waypoints": {}}
        i = 0
        for waypoint_obj in self.waypoints:
            coord = waypoint_obj.coordinate
            waypoint_dict = {"action": waypoint_obj.action}
            if waypoint_obj.coordinate:
                waypoint_dict["action_coordinate"] = {
                    "latitude": coord.latitude,
                    "longitude": coord.longitude,
                    "altitude": coord.altitude,
                }
            if waypoint_obj.heading:
                waypoint_dict["heading"] = waypoint_obj.heading
            if waypoint_obj.take_off_altitude:
                waypoint_dict["take_off_altitude"] = waypoint_obj.take_off_altitude
            result["waypoints"][(i)] = waypoint_dict
            i = i + 1
        return result


class Waypoint:
    # Waypoint Class stores waypoint information based on type of action.
    NOACTION = "NoAction"
    TAKEOFF = "Takeoff"
    GOTO = "GoTo"
    RTL = "RTL"
    LAND = "Land"
    PICTURE = "TakePicture"

    def __init__(
        self, action, geolocation=None, take_off_altitude=None, heading=None
    ) -> None:
        self.coordinate = geolocation
        self.action = action
        self.take_off_altitude = take_off_altitude
        self.heading = heading
