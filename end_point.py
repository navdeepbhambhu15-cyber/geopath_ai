import math
import json
from pathlib import Path


def calculate_endpoint(latitude, longitude, distance_meters, angle_degrees):
    """
    Calculate the endpoint using starting GPS coordinates,
    distance in meters, and bearing in degrees.
    
    0°   = North
    90°  = East
    180° = South
    270° = West
    """

    earth_radius = 6_371_000

    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)
    bearing = math.radians(angle_degrees)

    angular_distance = distance_meters / earth_radius

    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_distance)
        + math.cos(lat1) * math.sin(angular_distance)
        * math.cos(bearing)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(angular_distance)
        * math.cos(lat1),
        math.cos(angular_distance)
        - math.sin(lat1) * math.sin(lat2)
    )

    return {
        "latitude": math.degrees(lat2),
        "longitude": (math.degrees(lon2) + 540) % 360 - 180
    }


def save_endpoint(latitude, longitude, distance_meters,
                  angle_degrees, json_file="gps_data.json"):

    # Calculate the endpoint
    endpoint = calculate_endpoint(
        latitude,
        longitude,
        distance_meters,
        angle_degrees
    )

    # Create the JSON file's directory if necessary
    file_path = Path(json_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing JSON data, if available
    if file_path.exists():
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                data = {}

        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}

    # Save the endpoint without deleting other JSON entries
    data["endpoint"] = endpoint

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Endpoint calculated and saved!")
    print("Latitude:", endpoint["latitude"])
    print("Longitude:", endpoint["longitude"])
    print("Saved to:", file_path.resolve())

    return endpoint
def load_origin():
    try:
        with open("BUILDING_DATA.json") as f:
            o = json.load(f)["origin"]
        return o["latitude"], o["longitude"]
    except (FileNotFoundError, KeyError):
        return 28.5244, 77.1854

ORIGIN_LAT, ORIGIN_LON = load_origin()
with open("BUILDING_DATA.json") as f:
    start = json.load(f)["route_points"]["start"]

start_latitude = start["lat"]
start_longitude = start["lon"]

save_endpoint(
    latitude=start_latitude,
    longitude=start_longitude,
    distance_meters=300,
    angle_degrees=45,
    json_file="BUILDING_DATA.json")
    