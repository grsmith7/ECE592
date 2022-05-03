#### File contains functionality for image manipulation necessary
#### For preprocessing and scaling input photos for spot
#### Detection algorithms


import cv2
import math
import numpy as np
from image_helper_functions import *


def showImage(image, debug):
    ### Debug function to show image progression
    if debug == 0:
        return

    cv2.imshow("fun", cv2.resize(image, (540, 660)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return


def getColorMask(img):
    ### Get grey color mask of input image

    height = img.shape[0]
    width = img.shape[1]

    cv2.rectangle(img,(0,0),(width, height // 4),(255,255,255),-1)


    ## If needed when the lot is a darker color, or not picking up a good mask. (blank mask)
    b = img[height // 2, width // 2, 0]
    g = img[height // 2, width // 2, 1]
    r = img[height // 2, width // 2, 2]


    ## Set for grey only - BGR
    lower = np.uint8([115, 115, 90]) #Lighter Blues, textures
    upper = np.uint8([190, 255, 255]) #Darker Reds
    gray_mask = cv2.inRange(img, lower, upper)

    ## Spot mask to get areas missed do to noise from vehicles
    lower = np.uint8([90, 90, 90])
    upper = np.uint8([115, 115, 115])
    spot_mask = cv2.inRange(img, lower, upper)

    ## Get mask
    mask = cv2.bitwise_or(gray_mask, spot_mask)
    masked = cv2.bitwise_and(img, img, mask=mask)


    return masked


def convert2BW(image):
    ### Converts image to black and white

    ## Convert to Grayscale image
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ## Convert to black and white
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 80, 255, cv2.THRESH_BINARY)

    return blackAndWhiteImage


def imageMorph(image):
    ### Performs iamge manipulation functions
    kernel = np.ones((5, 5), np.uint8)
    morphed = image

    ## Closes wholes in image by calling OpenCV manipulation functions ons blackAndWhiteMask
    morphed = close(morphed, kernel, 3)
    morphed = erode(morphed, kernel,7)
    morphed = open(morphed, kernel, 6)
    morphed = dilate(morphed, kernel, 7)
    morphed = dilate(morphed,kernel,3)

    return morphed


def getContours(image, morphed):
    ### Finds contours of provided Black and White Mask

    ## Find edges
    edged = cv2.Canny(morphed, 30, 200)

    ## Find contours
    contours, hierarchy = cv2.findContours(
        edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    ## Draw contours on image
    img = image.copy()
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    return img


### Helper functions for finding best corners
def dist_to_top_left(image, x, y):
    ### Finds distance from images top left
    height = image.shape[0]
    width = image.shape[1]
    distance = math.sqrt(x**2 + 1.5*y**2)
    return distance


def dist_to_top_right(image, x, y):
    ### Finds distance from images top right
    height = image.shape[0]
    width = image.shape[1]
    x = width - x
    distance = math.sqrt(x**2 + 1.5*y**2)
    return distance


def dist_to_bot_right(image, x, y):
    ### Finds distance from images bot right
    height = image.shape[0]
    width = image.shape[1]
    x = width - x
    y = height - y
    distance = math.sqrt(x**2 + y**2)
    return distance


def dist_to_bot_left(image, x, y):
    ### Finds distance from images bot left
    height = image.shape[0]
    width = image.shape[1]
    y = height - y
    distance = math.sqrt(x**2 + y**2)
    return distance


def findBestCorners(image, morphed):
    ### Detects 4 most likely candidates for image corners of
    ### Black and White Mask
    ### Output list in format of [ b_l, b_r, t_l, t_r]

    ## Find all possible corners
    corners = cv2.goodFeaturesToTrack(morphed, 100, 0.00000000000000000001, 1)
    corners = np.int0(corners)
    img2 = image.copy()
    img3 = image.copy()

    ## Get image data
    height = img2.shape[0]
    width = img2.shape[1]

    ## Initialize to farthest away possible corner
    bot_left = [width, 0]
    bot_right = [0, 0]
    top_left = [width, height]
    top_right = [0, height]

    ## iterate through and find most likely candidate for each corner
    for corner in corners:
        x, y = corner.ravel()


        if dist_to_bot_left(image, x, y) < dist_to_bot_left(
            image, bot_left[0], bot_left[1]
        ):
            bot_left[0] = x
            bot_left[1] = y
            

        if dist_to_bot_right(image, x, y) < dist_to_bot_right(
            image, bot_right[0], bot_right[1]
        ):
            bot_right[0] = x
            bot_right[1] = y
            

        if dist_to_top_left(image, x, y) < dist_to_top_left(
            image, top_left[0], top_left[1]
        ):
            top_left[0] = x
            top_left[1] = y
            

        if dist_to_top_right(image, x, y) < dist_to_top_right(
            image, top_right[0], top_right[1]
        ):
            top_right[0] = x
            top_right[1] = y
            
        ## Draw most recent corner
        cv2.circle(img2, (x, y), 5, (0, 0, 255), -1)





    ## Draw corners on image
    cv2.circle(img2, (bot_left[0], bot_left[1]), 5, (0, 255, 0), -1)

    cv2.circle(img2, (bot_right[0], bot_right[1]), 5, (0, 255, 0), -1)

    cv2.circle(img2, (top_left[0], top_left[1]), 5, (0, 255, 0), -1)

    cv2.circle(img2, (top_right[0], top_right[1]), 5, (0, 255, 0), -1)

    cornered = img2

    corneredList = [bot_left, bot_right, top_left, top_right]

    return cornered, corneredList


def scaleImage(image, cornerList):
    ### Takes input of image and list of corners to scale
    ### to appear as if taken from above

    rows, cols, ch = image.shape

    ## List of original points and where they should go in new image
    ## Format is [ b_l, b_r, t_l, t_r]
    pts1 = np.float32([cornerList[0], cornerList[1], cornerList[2], cornerList[3]])

    pts2 = np.float32([[0, rows], [cols, rows], [0, 0], [cols, 0]])

    ## Scaling of image
    M = cv2.getPerspectiveTransform(pts1, pts2)
    scaled = cv2.warpPerspective(image, M, (cols, rows))

    return scaled
