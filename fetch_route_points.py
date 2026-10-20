import os
import json
from tinyfish import TinyFish

client = TinyFish(api_key=os.environ["TINYFISH_API_KEY"])


start_building = input(" Qutub minar")

route_points = {}

for label, name in [("start", start_building)]:
    print(f"Looking up location for: {name}")
    response = client.agent.run(
        goal=f"Find the latitude and longitude coordinates of {name}",
        url=f"https://www.google.com/search?q={name}+latitude+longitude+coordinates",
        output_schema={
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            }
        }
    )
    lat = response.result["latitude"]
    lon = response.result["longitude"]
    print(f"{name}: lat={lat}, lon={lon}")
    route_points[label] = {"name": name, "lat": lat, "lon": lon}

try:
    with open("BUILDING_DATA.json") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

data["route_points"] = route_points

with open("BUILDING_DATA.json", "w") as f:
    json.dump(data, f, indent=4)

print("Saved route points to BUILDING_DATA.json")