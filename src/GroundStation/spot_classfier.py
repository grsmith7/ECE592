import cv2 as cv2
from cv2 import waitKey
from cv2 import destroyAllWindows
import numpy as np
from keras.models import load_model
import tensorflow as tf


class SpotClassifier:
    '''Object to handle classification of image bounding boxes using pretrained CNN classifier model'''
    def __init__(self) -> None:
        tf.get_logger().setLevel("ERROR")
        self.model = load_model("parking_spots_detector/car1.h5") # Load Model
        self.class_dictionary = {0: "empty", 1: "occupied"} # Initialize classification dictionary

    def classify_boxes(self, image_path, bounding_boxes):
        '''Given a list of bounding boxes and the straightened image path, 
        return a dictionary of occupied and empty bounding boxes'''
        results = {"occupied": [], "empty": []}
        image = cv2.imread(image_path) #Read Image
        print("Classifiying " + str(len(bounding_boxes))+ " images")
        for box in bounding_boxes:
            snip = self.create_snippet(image, box) #Snip image using bounding box
            label = self.classify_snippet(snip) #Classify snippet with label of empty or occupied
            box_obj = {"bounding_box": box} # Create bounding_box dictionary
            results[label].append(box_obj) # Add bounding_box dictionary to label list
        
        return results

    def create_snippet(self, image, bounding_box):
        x_min, x_max, z_min, z_max = bounding_box
        snippet = image[z_min:z_max, x_min:x_max]
        snippet = cv2.resize(snippet, (48, 48))
        return snippet

    def classify_snippet(self, snippet):
        # Rescale image
        img = snippet / 255.0

        # Convert to a 4D tensor
        image = np.expand_dims(img, axis=0)

        # make predictions using the preloaded model
        class_predicted = self.model.predict(image)
        inID = np.argmax(class_predicted[0])
        
        #Convert label from 1 to occupied and 0 to empty and return
        label = self.class_dictionary[inID]
        return label
