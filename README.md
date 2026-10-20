# GeoNavigation.AI

A drone path-planning system that turns real GPS coordinates into a safe, battery-aware flight route. An AI agent (TinyFish) fetches real-world building and drone data from the live web, and A* pathfinding plans around the obstacles.

## The problem
while navigating a drone manually it will have human error and energy loses due to irreglarites in navigation.
Drone delivery routes must avoid tall buildings and no-fly zones, and must fit within the drone's battery. Obstacle and drone data is usually hardcoded or entered by hand.

##the solution
a program that is integrated with ai agent like tinyfish that will give path and minimum battery needed to perform task to avoid errors and energy losses

## What it does
- Converts real GPS coordinates (start and destination) into a grid.
- Uses **TinyFish** to fetch real building heights and real drone specs (DJI FlyCart 30, 29 min flight time) from the web.
- Blocks buildings taller than the drone's max flight height and plans around them with **A\***.
- Calculates one-way distance, round trip, flight time, battery used, and the minimum battery needed at takeoff, keeping a 20% reserve.
- Supports **date-based no-fly zones** (VIP flights, events) and **permanent zones** (e.g. a village), shown in red and orange.
- Shows the route live in a pygame window.

## How TinyFish is used
TinyFish acts as the AI agent that retrieves live web data:
- `fetch_building.py`: fetches building heights for obstacle cells.
- `drone_specification.py`: fetches the drone's flight time, which drives the battery calculation.
- `fetch_route_points.py`: looks up GPS coordinates for route points.

Limitation: for less-famous places TinyFish sometimes returned wrong coordinates, so the demo start point (Qutub Minar, 28.5244, 77.1854) is verified and set manually in `BUILDING_DATA.json`.

## Files
| File | Purpose |
|---|---|
| `gps_maps.py` | Main program: GPS to grid, A*, battery report, pygame display |
| `fetch_building.py` | TinyFish fetch of building heights |
| `drone_specification.py` | TinyFish fetch of drone specs |
| `fetch_route_points.py` | TinyFish fetch of route points |
| `end_point.py` | Calculates the destination from start, distance and bearing |
| `BUILDING_DATA.json` | Shared data file used by all scripts |

## How to run
1. Install: `pip install pygame`and 'pip install tinyfish'
2. Run `fetch_building.py` first. It overwrites `BUILDING_DATA.json`, it stores building heihts in json file(i used famous buildings so tinyfish agent can fetch it easily and the coordinates are real places relative to initial position.
3. Run `drone_specification.py`. it will ask tiny fish to fetch information about specific drone model like max weight and total flight time and it will be stored in json file mentioned
4. Run 'fetch_route_points.py' . enter name of a famous place like i have written qutub minar and tinyfish will fetch its longitude and latitude and it will be saved in json file 
5. Run `end_point.py`put' start position latitude and longitude there to calculate and save the destination's latitude and logitude in json file 
6. Run `gps_maps.py` and enter a flight date (e.g. `2026-10-20` to see the VIP no-fly zone). it will take data from json file and will show to path and battery needed

## Revenue model
 delivery and logistics companies pay per planned route or a monthly subscription; city authorities license the no-fly zone layer.like 5dollar per route for companies like amazon or people will pay on app for route.


Python, pygame, TinyFish
