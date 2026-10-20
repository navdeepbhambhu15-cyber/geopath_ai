import os
import json
from tinyfish import TinyFish

client = TinyFish(api_key=os.environ["TINYFISH_API_KEY"])

drone_models = ["DJI FlyCart 30"]

drone_specs = {}

for model in drone_models:
    print(f"Looking up specs for: {model}")
    response = client.agent.run(
        goal=f"Find the maximum flight time in minutes and maximum payload weight in kilograms for the {model} drone",
        url=f"https://www.google.com/search?q={model}+specifications+flight+time+payload",
        output_schema={
            "type": "object",
            "properties": {
                "flight_time_min": {"type": "number"},
                "payload_kg": {"type": "number"}
            }
        },

    )
    payload = response.result["payload_kg"]
    flight_time = response.result["flight_time_min"]
    drone_specs[model] = {"flight_time_min": flight_time, "payload_kg": payload}
    print(f"{model} specs: {response}")
    

try:
    with open("BUILDING_DATA.json") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

data["drone_specs"] = drone_specs

with open("BUILDING_DATA.json", "w") as f:
    json.dump(data, f, indent=4)

print("Saved all drone specs to BUILDING_DATA.json")