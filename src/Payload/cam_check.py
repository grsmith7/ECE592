import cv2
from cv2 import VideoCapture

def cam_check():
    cam = VideoCapture(-1)   #index of camera
    s, img = cam.read()
    if s:
        print('Camera connected successfully')
        return True
    else:
        print('ERROR: Camera not connected')
        return False
