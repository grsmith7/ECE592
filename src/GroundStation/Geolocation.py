from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Geolocation:
    ## Class to contain latitude, longitude and optional altitude point as float for easier use later.
    latitude: float = None
    longitude: float = None
    altitude: Optional[float] = None

    def __init__(self, coordinates) -> None:
        self.latitude = coordinates["latitude"]
        self.longitude = coordinates["longitude"]
        if "altitude" in coordinates:
            self.altitude = coordinates["altitude"]
        else:
            self.altitude = None

    def from_dict(obj) -> None:
        assert isinstance(obj, dict)
        latitude = obj.get("latitude")
        longitude = obj.get("longitude")
        if "altitude" in obj:
            altitude = obj.get("altitude")
        else:
            altitude = None
        return Geolocation(obj)

    def to_dict(self):
        result = {}
        result["latitude"] = self.latitude
        result["longitude"] = self.longitude
        result["altitude"] = self.altitude
        return result
