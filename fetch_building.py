import json
import os
from tinyfish import TinyFish

client = TinyFish(api_key=os.environ["TINYFISH_API_KEY"])

# Name -> grid cell position (col, row)
building_positions = {
    "Eiffel Tower": (23, 12),
    "Burj Khalifa": (24, 12),
    "Shanghai Tower": (24,13),
    "taj hotel ": (25, 13),
    " Taipei 101":( 19,9),
    " one world trade centre":(20,9),
    "petronas towers":(19,10),
    " Tokyo Tower":(20,10),
    "The Shard":(19,18),
    "Lotte World tower":( 20,18),
    "Jeddah Tower":( 19,19),
    "Shanghai World Financial centre":(20,19),


}

building_data = {}

for name, cell in building_positions.items():
    print("Looking up:", name)
    response = client.agent.run(
        goal=f"Find the height in meters of {name}. Search online for it.",
        url="https://www.google.com/search?q=" + name.replace(" ", "+") + "+height+in+meters",
        output_schema={
            "type": "object",
            "properties": {
                "height_m": {"type": "number"},
            },
            "required": ["height_m"],
        },
    )

    if response.status.name == "COMPLETED":
        height = response.result["height_m"]
        print(name, "height:", height)
        building_data[f"{cell[0]},{cell[1]}"] = height
    else:
        print(name, "failed:", response.error.message)

with open("BUILDING_DATA.json", "w") as f:
    json.dump(building_data, f)

print("Saved all buildings to BUILDING_DATA.json")