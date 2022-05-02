import cv2
from cv2 import VideoCapture
from libsvm import svmutil
from brisque import BRISQUE
from dronekit import VehicleMode

# Constants used in function

IQA_THRESHOLD = 40  # image quality threshold (0-100); decrease for higher quality


def take_picture(vehicle, waypoint_num):

    # initialize image quality program
    # initialize the camera
    cam = VideoCapture(-1)  # index of camera
    s, img = cam.read()
    test_score = IQA_THRESHOLD + 5  # initial value
    if s:  # frame captured without any errors
        while test_score > IQA_THRESHOLD:  # take pictures until good quality
            cv2.imwrite(f"/home/pi/image{waypoint_num}.jpg", img)  # saves locally
            brisq = BRISQUE(f"/home/pi/image{waypoint_num}.jpg")
            test_score = brisq.score()  # returns num from 0-100
            # print(test_score) #lower number = less distortion
            # print statement for testing purposes
            if test_score > IQA_THRESHOLD:
                s, img = cam.read()  # take another picture if too blurry
    cv2.imwrite(
        f"/home/pi/public/image{waypoint_num}.jpg", img
    )  # save final pic in shared drive
    file_data = open(f"/home/pi/public/data{waypoint_num}.txt", "x")
    alt = vehicle.location.global_relative_frame.alt
    lat = vehicle.location.global_relative_frame.lat
    lon = vehicle.location.global_relative_frame.lon
    #get drone data and store in text file
    file_data.write(
        "Altitude = "
        + str(alt)
        + "\n"
        + "Lattitude = "
        + str(lat)
        + "\n"
        + "Longitude = "
        + str(lon)
    )
    file_data.close()