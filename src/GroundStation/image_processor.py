from threading import currentThread
import cv2
import numpy as np
import math
from image_manipulation import *
from location_finder import LocationFinder
from spot_detection_functionality import *
from fish import fish
from imageio import imread, imwrite


class ImageProcessor:
    def __init__(self) -> None:
        pass

    def preprocess_data(self, image_path):
        image = imread(image_path)
        pathSplit = image_path.split("/")
        name = pathSplit[-1]
        name = name[0:-3]
        # Remove fisheye from image]
        output_img = fish(image, -0.06)
        new_path = "dist/" + name + "png"
        imwrite(new_path, output_img, format="png")
        return new_path

    def load_images(self, images_path):
        images = []
        for i in images_path:
            images.append(cv2.imread(i))
        return images

    def identify_parking_spot_bounding_boxes(self, images_path, input_object):
        # Input Processed Mission Data
        # Output Bounding Boxes (list of 4 corners)

        # Variable to specify if debug functions are on or off
        debug = 0

        # Kernel used for sharpening
        kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

        # Remove Fisheye
        distorted_image_paths = []
        for image_path in images_path:
            newPath = self.preprocess_data(image_path)
            distorted_image_paths.append(newPath)
        # Load images that are to be used
        images = self.load_images(distorted_image_paths)

        for image in images:
            showImage(image, debug)

            # Apply filters
            bilateral = cv2.bilateralFilter(image, 30, 4500, 35)

            showImage(bilateral, debug)

            # Make mask of lot
            mask = getColorMask(bilateral)

            showImage(mask, debug)

            # Convert to black and white
            blackAndWhite = convert2BW(mask)

            showImage(blackAndWhite, debug)

            # Perform mask manipulation
            morphed = imageMorph(blackAndWhite)

            showImage(morphed, debug)

            # Canny edge detection
            contour = getContours(image, morphed)

            showImage(contour, debug)

            # Find best corners
            cornered, cornerList = findBestCorners(image, morphed)

            showImage(cornered, debug)

            # Format image
            scaled = scaleImage(image, cornerList)

            showImage(scaled, debug)

            # Find Parking Columns
            location_object = LocationFinder()

            cv2.imwrite("test_scaled.PNG", scaled)
            columns, rects = findColumns(scaled, location_object, input_object)

            showImage(columns, 1)
            return rects
        pass
