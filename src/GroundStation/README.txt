Code Directory for Parking Spots Detector
This directory contains the code ran on the ground station that is responsible for creating the mission, communicating with the payload, and processing the images on the ground station.

main.py - This file contains the main function and calls functions to create the mission, communicate with the payload. and process images.
car1.h5 - This file stores the keras model that is responsible for classifying parking spot images as occupied or empty. It was created from the parking spot tutorial code.
fish.py - This file contains code from the Gil-Mor/iFish
Geolocation.py - This file contains the class that represents a location in geographical coordinates.
image_helper_functions.py - This file contains various mask manipulation functions.
image_manipulation.py - This file contains helper functions used to morph and scale the image.
image_processor.py - This file contains the class used to process the image and scale it.
input.json - This file contains the information necessary to execute the program. The corners of the parking lot must start in the bottom right corner and go clockwise.
location_finder.py - This file contains the class used to label the parking lot spaces.
mission_creator.py - This file contains the class used to create the mission object.
/Mission Data - Directory to store data copied from share drive during processing.
/Test Images - Images used during testing from Google Maps, Apple Maps, Bing Maps, and Images taken from Testing.
Mission.py - This file contains the class that represents a mission as a series of waypoints and a class that represents a waypoint and its attributes.
payload.py - This file contains the class that handles communication and data transfer to the companion computer from the perspective of the ground station.
spot_classifier.py - This file contains the class that handles classifying parking spaces using a pre-trained Keras Model.
spot_detection_functionality.py - This file contains the function to find the bounding boxes of the parking spaces given the scaled image.
userinput.py - This file contains the class that handles reading in the user input from input.json.
