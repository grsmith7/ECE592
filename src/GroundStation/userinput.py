import json
from Geolocation import Geolocation
from typing import Callable, List


class UserInputOver:
    # Get user input from json file and package as a python object for easy retrieval
    def __init__(self) -> None:
        pass

    def get_user_input(self, path):
        ##Read in inputs from specified json path
        with open(path) as f:
            input_dict = json.load(f)
        # Use method from app.quicktype.io to convert json to object
        self.input_object = UserInput_from_dict(input_dict)


##Boiler plate code from app.quicktype.io to convert json files to python objects.

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, float) and not isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class ParkingLotCorners:
    corners: List[Geolocation]

    @staticmethod
    def from_dict(obj: Any) -> "ParkingLotCorners":
        assert isinstance(obj, dict)
        corners = from_list(Geolocation.from_dict, obj.get("corners"))
        return ParkingLotCorners(corners)

    def to_dict(self) -> dict:
        result: dict = {}
        result["corners"] = from_list(lambda x: to_class(Geolocation, x), self.corners)
        return result


@dataclass
class UserInput:
    parking_lot_bounding_box: ParkingLotCorners
    picture_altitude: float
    number_of_lanes: int
    standoff_distance: float
    number_of_waypoints: int

    @staticmethod
    def from_dict(obj: Any) -> "UserInput":
        assert isinstance(obj, dict)
        parking_lot_bounding_box = ParkingLotCorners.from_dict(
            obj.get("parking_lot_corners")
        )
        picture_altitude = from_float(obj.get("pictureAltitude"))
        number_of_lanes = from_int(obj.get("numberOfLanes"))
        standoff_distance = from_float(obj.get("standoffDistanceinFT"))
        number_of_waypoints = from_int(obj.get("numberOfWaypoints"))
        return UserInput(
            parking_lot_bounding_box,
            picture_altitude,
            number_of_lanes,
            standoff_distance,
            number_of_waypoints,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["parking_lot_bounding_box"] = to_class(
            ParkingLotCorners, self.parking_lot_bounding_box
        )
        result["pictureAltitude"] = from_float(self.picture_altitude)
        result["numberOfLanes"] = from_int(self.number_of_lanes)
        result["standoffDistance"] = from_float(self.standoff_distance)
        result["numberOfWaypoints"] = from_int(self.number_of_waypoints)
        return result


def UserInput_from_dict(s: Any) -> UserInput:
    return UserInput.from_dict(s)


def UserInput_to_dict(x: UserInput) -> Any:
    return to_class(UserInput, x)
