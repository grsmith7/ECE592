#### File contains functionality for spot detection algorithm to
#### identify open spots in scaled input images
import cv2
import os, glob
import numpy as np
import math


def findColumns(image, location_object, input_object):
    ### Function to find columns in scaled image and return
    ### List of rectangles and image with columns printed on it
    columns = image.copy()
    rects = []

    image_height = image.shape[0]
    image_width = image.shape[1]

    ## Values for dimensions of spot widths and lengths
    SPOTWIDTH = 9.25
    SPOTHEIGHT = 25
    LANEWIDTH = 16
    LANEHEIGHT = 17

    (
        width,
        width_unit_vector,
        height,
        height_unit_vector,
        origin_point,
    ) = location_object.calculate_lot_geometry(input_object)
    ## Convert width and height to feet
    widthInFeet = width / ((0.3048 / 1.11) * 0.00001)
    height_in_feet = height / ((0.3048 / 1.11) * 0.00001)

    ## Convert width and heigth to pixels
    spot_width_in_pixels = round(SPOTWIDTH * (image_width / widthInFeet))
    spot_height_in_pixels = round(SPOTHEIGHT * (image_height / height_in_feet))

    print("width_in_feet: ", widthInFeet)
    ## Find length of spot lanes
    lane_length = widthInFeet - 2 * LANEWIDTH

    print("lane_length: ", lane_length)
    ## Find number of spots
    number_of_spots = int(round(lane_length / SPOTWIDTH))

    print("number_of_spots: ", number_of_spots)
    ## Find spots bounding boxes
    fraction_box_xs = [
        (float(x) * SPOTWIDTH + LANEWIDTH) / widthInFeet
        for x in range((number_of_spots))
    ]

    feet_box_ys = []

    feet_box_ys.append(0)  # First half-lane
    first_lane_start_y = feet_box_ys[0] + SPOTHEIGHT + LANEHEIGHT

    for i in range(input_object.number_of_lanes - 1):
        lane_top = first_lane_start_y + i * (2 * SPOTHEIGHT + LANEHEIGHT)
        lane_bottom = lane_top + SPOTHEIGHT
        feet_box_ys.append(lane_top)
        feet_box_ys.append(lane_bottom)
    feet_box_ys.append(height_in_feet - 3 * SPOTHEIGHT - 37)
    feet_box_ys.append(height_in_feet - 2 * SPOTHEIGHT - 37)
    feet_box_ys.append(height_in_feet - SPOTHEIGHT)  # Add Last height

    fraction_box_ys = [(y / height_in_feet) for y in feet_box_ys]

    # Convert to pixel measurments
    pixel_box_xs = [round(x * image_width) for x in fraction_box_xs]

    pixel_box_ys = [round(y * image_height) for y in fraction_box_ys]

    ## Establish spot where first lane starts to add boundry lanes later
    first_x = pixel_box_xs[0]

    first_y = pixel_box_ys[0]

    for x_min in pixel_box_xs:
        for y_min in pixel_box_ys:
            rects.append(
                [
                    x_min,
                    x_min + spot_width_in_pixels,
                    y_min,
                    y_min + spot_height_in_pixels,
                ]
            )
            columns = cv2.rectangle(
                columns,
                (x_min, y_min),
                (x_min + spot_width_in_pixels, y_min + spot_height_in_pixels),
                (0, 255, 0),
                3,
            )

    ### Code to add boundry lanes that extend beyond normal length
    ## Top Left Boxes
    for i in range(int(first_x // spot_width_in_pixels)):
        columns = cv2.rectangle(
            columns,
            (first_x - spot_width_in_pixels * (i + 1), first_y),
            (first_x + spot_width_in_pixels * i, first_y + spot_height_in_pixels),
            (0, 255, 0),
            3,
        )
        rects.append(
            [
                first_x - spot_width_in_pixels * (i + 1),
                first_x + spot_width_in_pixels * i,
                first_y,
                first_y + spot_height_in_pixels,
            ]
        )

    ## Top Right Boxes
    for i in range(int((image_width - x_min) // spot_width_in_pixels)):
        columns = cv2.rectangle(
            columns,
            (x_min + spot_width_in_pixels * (i), first_y),
            (x_min + spot_width_in_pixels * (i + 1), first_y + spot_height_in_pixels),
            (0, 255, 0),
            3,
        )
        rects.append(
            [
                x_min + spot_width_in_pixels * (i),
                x_min + spot_width_in_pixels * (i + 1),
                first_y,
                first_y + spot_height_in_pixels,
            ]
        )

    ## Bot Left Boxes
    for i in range(int(first_x // spot_width_in_pixels)):
        columns = cv2.rectangle(
            columns,
            (first_x - spot_width_in_pixels * (i + 1), y_min),
            (first_x + spot_width_in_pixels * i, y_min + spot_height_in_pixels),
            (0, 255, 0),
            3,
        )
        rects.append(
            [
                first_x - spot_width_in_pixels * (i + 1),
                first_x + spot_width_in_pixels * i,
                y_min,
                y_min + spot_height_in_pixels,
            ]
        )

    ## Bot  Right Boxes
    for i in range(int((image_width - x_min) // spot_width_in_pixels)):
        columns = cv2.rectangle(
            columns,
            (x_min + spot_width_in_pixels * (i), y_min),
            (x_min + spot_width_in_pixels * (i + 1), y_min + spot_height_in_pixels),
            (0, 255, 0),
            3,
        )
        rects.append(
            [
                x_min + spot_width_in_pixels * (i),
                x_min + spot_width_in_pixels * (i + 1),
                y_min,
                y_min + spot_height_in_pixels,
            ]
        )

    return columns, rects
