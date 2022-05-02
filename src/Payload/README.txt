Code Directory for Payload
This directory contains the code ran on the companion computer that is responsible for taking pictures, communicating with the autopilot, and storing data for ground station processing.

main.py - This file contains the main function and handles getting mission data and running the mission executor. This file is run to initialize the software.
cam_check.py - This file contains a function to ensure the camera is connected and ready to take pictures.
take_picture.py - This file contains a function to take a picture that meets a defined quality standard and store the picture in the shared directory.
communications_functions.py - This file contains functions used to load mission data from the shared directory.
mission_execution_functions.py - This file contains functions used to parse and execute the mission and interact with the autopilot.