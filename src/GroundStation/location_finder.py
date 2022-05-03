import math

import cv2

from Geolocation import Geolocation


class LocationFinder:
    def __init__(self) -> None:
        pass

    def find_locations(self, input_obj, img_path, classified_data):
        '''# Purpose: Find locations of labeled parking spots.
        # Inputs: Input object containing program inputs, img_path: path to perspectivized image, classified_data: dictionary contaning spots classfied as empty or occupied.
        # Outputs: Classified Dictionary with empty spots labeled with latitude and longitude'''
        (
            lot_width,
            lot_width_unit_vector,
            lot_height,
            lot_height_unit_vector,
            lot_origin_point,
        ) = self.calculate_lot_geometry(input_obj) # Calculate necessary lot geometry, similar to mission creator
        image = cv2.imread(img_path)
        image_width = image.shape[1] # Find width in px
        image_height = image.shape[0] # Find height in px
        for i in range(len(classified_data["empty"])):
            #Iterate through empty parking spots
            parking_space_box = classified_data["empty"][i]["bounding_box"]
            center_x, center_y = self.calculate_bounding_box_center(parking_space_box) #Calculate center of bounding box in px
            percent_height_from_lot_origin = (image_height - center_y) / image_height #Find percent height using px
            percent_width_from_lot_origin = (image_width - center_x) / image_width # Find percent width using px
            width_mag = lot_width * percent_width_from_lot_origin #Use percent of image to estabilish magnitude in width
            height_mag = lot_height * percent_height_from_lot_origin #Use percent of image to establish magnitude in height
            latitude = (
                width_mag * lot_width_unit_vector[0]
                + height_mag * lot_height_unit_vector[0]
                + lot_origin_point[0]
            ) #Use magnitude and basis vectors to find latitude
            longitude = (
                width_mag * lot_width_unit_vector[1]
                + height_mag * lot_height_unit_vector[1]
                + lot_origin_point[1]
            ) #Use magnitude and basis vectors to find longitude
            geo_dict = {"latitude": latitude, "longitude": longitude} # Create geographic dictionary
            classified_data["empty"][i]["location"] = Geolocation(geo_dict) # Add geolocation obj to classifed data dictionary
        return classified_data

    def find_locations2(self, input_obj, img_path, picture_data, classified_data):
        '''# Purpose: Find locations of labeled parking spots.
        # Inputs: Input object containing program inputs, img_path: path to perspectivized image, classified_data: dictionary contaning spots classfied as empty or occupied.
        # Outputs: Classified Dictionary with empty spots labeled with latitude and longitude'''
        (
            degree_width,
            width_unit_vector,
            degree_height,
            height_unit_vector,
            origin_point,
        ) = self.calculate_lot_geometry(input_obj) 
        image = cv2.imread(img_path)
        image_bounds = [0, image.shape[1], 0, image.shape[0]] #Find Image Bounds in pixels
        image_long_lat_zero = (image_bounds[1], image_bounds[3])  # Bottom Right corner in pixels
        pixel_width = image_bounds[1] - image_bounds[0] #width in pix
        pixel_height = image_bounds[3] - image_bounds[2] #height in pix
        pixel_to_degree_width = degree_width / pixel_width #Conversion factor from pixel to degrees in width dim
        pixel_to_degree_height = degree_height / pixel_height #Conversion factor from pixel to degrees in height dim
        for i in range(len(classified_data["empty"])):
            ## Iterate through each empty parking spot
            parking_space_box = classified_data["empty"][i]["bounding_box"]
            center_x, center_y = self.calculate_bounding_box_center(parking_space_box) #Find Center of bounding box 
            pixel_width_dist = image_long_lat_zero[0] - center_x #distance in px to edge on width
            pixel_height_dist = image_long_lat_zero[1] - center_y #distance in px to edge on hieght
            width_mag = pixel_width_dist * pixel_to_degree_width #Transform width to degrees
            height_mag = pixel_height_dist * pixel_to_degree_height #Transform height to degrees
            latitude = (
                width_mag * width_unit_vector[0]
                + height_mag * height_unit_vector[0]
                + origin_point[0]
            ) # Find latitude using linear basis
            longitude = (
                width_mag * width_unit_vector[1]
                + height_mag * height_unit_vector[1]
                + origin_point[1]
            ) # Find longitude using linear basis
            geo_dict = {"latitude": latitude, "longitude": longitude} # Create geographic dictionary
            classified_data["empty"][i]["location"] = Geolocation(geo_dict) # Add geolocation obj to classifed data dictionary
        return classified_data

    def calculate_lot_geometry(self, input_obj):
        #Calculate lot geometry, similar to Mission Creator code
        parking_lot = input_obj.parking_lot_bounding_box
        lat = [loc.latitude for loc in parking_lot.corners]
        long = [loc.longitude for loc in parking_lot.corners]
        points = list(zip(lat, long))
        parking_lot_edges = []
        for index in range(len((points))):
            currentPoint = points[index]
            previousPoint = points[index - 1]
            parking_lot_edges.append(math.dist(currentPoint, previousPoint))
        width = max(parking_lot_edges[1], parking_lot_edges[1])
        height = max(parking_lot_edges[0], parking_lot_edges[0])
        width_unit_vector = (
            (points[1][0] - points[0][0]) / parking_lot_edges[1],
            (points[1][1] - points[0][1]) / parking_lot_edges[1],
        )
        height_unit_vector = (
            (points[-1][0] - points[0][0]) / parking_lot_edges[0],
            (points[-1][1] - points[0][1]) / parking_lot_edges[0],
        )
        origin_point = points[0]
        return width, width_unit_vector, height, height_unit_vector, origin_point

    def calculate_bounding_box_center(self, bounding_box):
        #Calculate center of bounding box given [xmin,xmax,ymin,ymax]
        x = (bounding_box[1] - bounding_box[0]) / 2 + bounding_box[0]
        y = (bounding_box[3] - bounding_box[2]) / 2 + bounding_box[2]
        return x, y
