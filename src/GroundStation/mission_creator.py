import math
from Mission import Mission, Waypoint
from Geolocation import Geolocation


class MissionCreator:
    def __init__(self, user_input) -> None:
        self.input = user_input
        self.create_mission()

    def find_picture_heading(self):
        #This function finds the heading of the drone to take the picture. The heading should be 
        #perpendicular to the parking lot edge where the drone is taking pictures.
        parking_lot = self.input.parking_lot_bounding_box
        lat = [loc.latitude for loc in parking_lot.corners]
        long = [loc.longitude for loc in parking_lot.corners]
        points = list(zip(lat, long))
        starting_point = points[0]
        ending_point = points[-1]
        height_vector = (
            (ending_point[0] - starting_point[0]),
            (ending_point[1] - starting_point[1]),
        ) #Find height vector which is pointing in the perpendicular direction
        height_heading = math.degrees(math.atan2(height_vector[1], height_vector[0])) # Returns the angle of the height vector from -pi to pi
        #The following code converts the heading from (-180 to 180) to (0 to 360)
        if height_heading>=0:
            return height_heading
        elif height_heading<0:
            return 360+height_heading 

    def find_waypoint_coordinates(self):
        ## This function uses magnitudes of the edges of the parking lot to create waypoint
        ## coordinates for the mission.
        parking_lot = self.input.parking_lot_bounding_box
        lat = [loc.latitude for loc in parking_lot.corners]
        long = [loc.longitude for loc in parking_lot.corners]
        points = list(zip(lat, long))
        parking_lot_edges = []
        for index in range(len((points))):
            currentPoint = points[index]
            previousPoint = points[index - 1]
            parking_lot_edges.append(math.dist(currentPoint, previousPoint))
        standoff_distance_in_degrees = (
            self.input.standoff_distance /364000
        ) #Distance away from parking lot to take pictures
        width = parking_lot_edges[1] # The length of the width edge in degrees
        height = parking_lot_edges[0] # The length of the height edge in degrees 
        width_unit_vector = (
            (points[1][0] - points[0][0]) / parking_lot_edges[1],
            (points[1][1] - points[0][1]) / parking_lot_edges[1],
        ) #Vector that represents the latitude and longitude increase along the wide edge of the parking lot
        height_unit_vector = (
            (points[-1][0] - points[0][0]) / parking_lot_edges[0],
            (points[-1][1] - points[0][1]) / parking_lot_edges[0],
        )#Vector that represents the latitude and longitude increase along the height edge of the parking lot
        number_of_waypoints = self.input.number_of_waypoints
        waypoint_spacing = width / (number_of_waypoints + 1) # Waypoints evenly spaced along the width edge
        waypoint_height_mag = -1 * standoff_distance_in_degrees #Distance away from edge in height mag proportion
        waypoint_width_mags = [
            (i + 1) * waypoint_spacing for i in range(number_of_waypoints)
        ] # Create waypoint in width mag using waypoint spacings, starting at waypoint_spacing and ending at width-waypoint_spacing
        waypoint_coordinates = []
        for width_mag in waypoint_width_mags:
            #Convert width and hieght magnitude to latitude and longitude using edge vectors
            latitude = (
                width_mag * width_unit_vector[0]
                + waypoint_height_mag * height_unit_vector[0]
                + points[0][0]
            ) 
            longitude = (
                width_mag * width_unit_vector[1]
                + waypoint_height_mag * height_unit_vector[1]
                + points[0][1]
            )
            altitude = self.input.picture_altitude #altitude where picture is taken
            location = Geolocation(
                {"latitude": latitude, "longitude": longitude, "altitude": altitude}
            )
            waypoint_coordinates.append(location) #Add waypoint coordinate location to list
        return waypoint_coordinates

    def create_mission(self):
        waypoint_coordinates = self.find_waypoint_coordinates() #Get waypoint coordinates
        picture_heading = self.find_picture_heading() #Get picture heading (perpendicular to lot edge)
        self.construct_mission_object(
            waypoint_coordinates, self.input.picture_altitude, picture_heading
        ) #Construct mission object

    def construct_mission_object(
        self, waypoint_coordinates, take_off_altitude, picture_heading
    ):
        waypoints = []
        waypoints.append(
            Waypoint(Waypoint.TAKEOFF, take_off_altitude=take_off_altitude)
        )  # Add Take off instruction
        for coords in waypoint_coordinates:
            waypoints.append(
                Waypoint(Waypoint.GOTO, geolocation=coords)
            )  # Add Go-to coordinate instruction
            waypoints.append(
                Waypoint(Waypoint.PICTURE, heading=picture_heading)
            )  # Add take picture at a given heading instruction
        waypoints.append(Waypoint(Waypoint.RTL))  # Add RTL instruction
        self.mission_obj = Mission(waypoints) #Create Mission obj using instructions

    def export_mission(self):
        return self.mission_obj.export_mission_as_dict()
