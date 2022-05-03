import cv2


def dilate(image, kernel, rounds):
    ##Increases size of white blobs depending on number of rounds
    ### Takes input of image, kernel to be used for dilation and
    ### how many round wanted for dilation

    dilated = cv2.dilate(image, kernel, iterations = rounds)

    return dilated

def erode(image, kernel, rounds):
    ##Decrease size of white blobs depending on number of rounds
    ### Takes input of image, kernel to be used for erosion and
    ### how many round wanted for erosion

    eroded = cv2.erode(image, kernel, iterations = rounds)

    return eroded

def close(image, kernel, rounds):
    ##Similar to Dilate, but it closes white holes in image
    ### Takes input of image, kernel to be used for close and
    ### how many round wanted for close

    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations = rounds)

    return closed

def open(image, kernel, rounds):
    ## Similar to erode, enlarges holes in white blobs
    ### Takes input of image, kernel to be used for open and
    ### how many round wanted for open

    opened= cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations = rounds)

    return opened
