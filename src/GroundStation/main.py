import json

from cv2 import destroyAllWindows
from Geolocation import Geolocation
from location_finder import LocationFinder
import cv2

from spot_classfier import SpotClassifier
from userinput import UserInputOver
from payload import Payload
from image_processor import ImageProcessor
from mission_creator import MissionCreator
import os


def main():
    #Import User Input Data
    input_info = UserInputOver()
    input_info.get_user_input("parking_spots_detector/input.json")
    # Parking lot corners must be clockwise for mission creator picture heading to work

    #Create and Mission JSON
    mission_creator = MissionCreator(input_info.input_object)
    mission_dict = mission_creator.export_mission()

    # Make Debug False when connecting to the Payload
    debug = True
    data_path = "parking_spots_detector/Mission Data"

    if debug == False:
        payload = Payload()
        #Add Mission to Shared Drive
        payload.send_mission(mission_dict)
        #Wait for Mission Completion
        payload.wait_for_mission_completion()
        #Download Mission Data to Data Path
        payload_data = payload.receive_mission_data(data_path)

    # Create a list of image paths
    img_paths = []
    paths_inside = os.listdir(data_path)
    for pathI in paths_inside:
        if pathI[-3:] == "jpg":
            img_paths.append(data_path + "/" + pathI)

    #Process images and return boxes and scaled image
    img_processor = ImageProcessor()
    boxes = img_processor.identify_parking_spot_bounding_boxes(
        img_paths, input_info.input_object
    )
    perspectivized_image_path = "test_scaled.PNG"


    # Classify boxes using scaled image and boxes.
    classifier_obj = SpotClassifier()
    classified_boxes = classifier_obj.classify_boxes(perspectivized_image_path, boxes)

    # Find locations of classified boxes
    spot_location_finder = (
        LocationFinder()
    )  # Configured for Bottom right corner to be first
    locations = spot_location_finder.find_locations(
        input_info.input_object, perspectivized_image_path, classified_boxes
    )

    #Return list of locations and bounding boxes
    print(locations)

    # Show classified boxes
    img = cv2.imread(perspectivized_image_path)
    print(len(classified_boxes["empty"]))
    for box in classified_boxes["empty"]:
        xmin, xmax, ymin, ymax = box["bounding_box"]
        img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
    cv2.imwrite("classified.jpg", img)
    cv2.imshow("fun", cv2.resize(img, (540, 660)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
