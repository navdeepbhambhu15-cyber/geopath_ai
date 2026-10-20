print( " drone path planner started" )
import pygame
import heapq
import json
restricted_zones = [
    {"name": "VIP flight zone", "dates": ["2026-10-20", "2026-10-21"],
     "cells": [(24, 8), (25, 8), (24, 9), (25, 9)]},
    {"name": "Event area", "dates": ["2026-10-25"],
     "cells": [(28, 4), (29, 4), (28, 5), (29, 5)]},
]
permanent_restricted_zones = [{"name": "Kishangarh Village", "cells": [(c, r) for c in range(10, 15) for r in range(13, 18)]}]

flight_date = input("Enter flight date (YYYY-MM-DD): ").strip()
def initialize_d_star():
 pygame.init()
CELL=20
WIDTH = 800
HEIGHT =600
COLS = WIDTH//CELL
ROWS = HEIGHT//CELL
DRONE_MAX_HEIGHT=15
METERS_PER_CELL=20
import json
with open("BUILDING_DATA.json") as f:
    _data = json.load(f)

ORIGIN_LAT = _data["route_points"]["start"]["lat"]
ORIGIN_LON = _data["route_points"]["start"]["lon"]
END_LAT = _data["endpoint"]["latitude"]
END_LON = _data["endpoint"]["longitude"]
def gps_to_cell(lat, lon):
    meters_per_deg_lat = 111000
    meters_per_deg_lon = 111000 * math.cos(math.radians(ORIGIN_LAT))
    north_m = (lat - ORIGIN_LAT) * meters_per_deg_lat
    east_m = (lon - ORIGIN_LON) * meters_per_deg_lon
    col = int(east_m / METERS_PER_CELL)+20
    row = int(-north_m / METERS_PER_CELL)+15
    return (col, row)

def load_building_heights():
    try:
        with open("BUILDING_DATA.json") as f:
            raw = json.load(f)
        heights = {}
        for k, h in raw.items():
            parts = k.split(",")
            if len(parts) == 2 and all(p.strip().lstrip("-").isdigit() for p in parts):
                heights[tuple(map(int, parts))] = h
        return heights
    except FileNotFoundError:
        return {}

building_heights = load_building_heights()



blocked = {
    cell
    for cell, height in building_heights.items()
    if height > DRONE_MAX_HEIGHT
}
restricted_cells = set()
for zone in restricted_zones:
    if flight_date in zone["dates"]:
        restricted_cells.update(zone["cells"])
        print(f"Restricted today: {zone['name']}")

blocked.update(restricted_cells)
for zone in permanent_restricted_zones:
    blocked.update(set(zone["cells"]))


def to_cell(x, y):
    return (x // CELL, y // CELL)

def to_pixel(cell):
 return (cell[0] * CELL + CELL // 2, cell[1] * CELL + CELL // 2)
import math

def heuristic(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def astar(start, goal, blocked):
    directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
    open_heap = [(heuristic(start, goal), 0, start)]
    came_from = {}
    g_cost = {start: 0}

    while open_heap:
        _, cost, current = heapq.heappop(open_heap)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        if cost > g_cost[current]:
            continue

        for dx, dy in directions:
            nxt = (current[0] + dx, current[1] + dy)
            if not (0 <= nxt[0] < COLS and 0 <= nxt[1] < ROWS):
                continue
            if nxt in blocked:
                continue

            step = math.sqrt(2) if dx != 0 and dy != 0 else 1
            new_cost = cost + step
            if new_cost < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(open_heap, (new_cost + heuristic(nxt, goal), new_cost, nxt))

    return None
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Path Planner")

WHITE = (255, 255, 255)
BLUE = (40, 100, 255)
BLACK = (0, 0, 0)



running = True
start_cell = gps_to_cell(ORIGIN_LAT, ORIGIN_LON)
goal_cell = gps_to_cell(END_LAT, END_LON)
goal_px = to_pixel(goal_cell)
drone_x, drone_y = to_pixel(start_cell)
path = astar(start_cell, goal_cell, blocked)
# ---------- Battery calculation ----------
METERS_PER_CELL = 20       # 1 grid cell = 20 meters
def load_drone_specs():
    try:
        with open("BUILDING_DATA.json") as f:
            raw = json.load(f)
        specs = raw.get("drone_specs", {})
        if specs:
            first_drone = next(iter(specs.values()))
            return first_drone["flight_time_min"]
    except FileNotFoundError:
        pass
    return 30

DRONE_SPEED_MS = 10
DRONE_FLIGHT_MIN = load_drone_specs()
RESERVE_PERCENT = 20       # battery that must remain after returning

def path_length_m(path):
    total = 0
    for a, b in zip(path, path[1:]):
        total += math.hypot(b[0] - a[0], b[1] - a[1]) * METERS_PER_CELL
    return total

if path:
    one_way_m = path_length_m(path)
    round_trip_m = one_way_m * 2
    flight_time_min = round_trip_m / DRONE_SPEED_MS / 60
    battery_used = flight_time_min / DRONE_FLIGHT_MIN * 100
    min_battery_needed = battery_used + RESERVE_PERCENT

    print(f"One-way distance: {one_way_m:.0f} m")
    print(f"Round trip: {round_trip_m:.0f} m")
    print(f"Flight time: {flight_time_min:.1f} min")
    print(f"Battery used: {battery_used:.1f}%")
    print(f"Minimum battery needed at takeoff: {min_battery_needed:.1f}%")

    try:
        with open("BUILDING_DATA.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data["battery_report"] = {
        "one_way_m": round(one_way_m, 1),
        "round_trip_m": round(round_trip_m, 1),
        "flight_time_min": round(flight_time_min, 1),
        "battery_used_percent": round(battery_used, 1),
        "min_battery_needed_percent": round(min_battery_needed, 1)
    }

    with open("BUILDING_DATA.json", "w") as f:
        json.dump(data, f, indent=4)
path_px = [to_pixel(c) for c in path] if path else []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    # Draw the grid
    for col in range(COLS):
        x = col * CELL
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))

    for row in range(ROWS):
        y = row * CELL
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))
    for cell in blocked :
        pygame.draw.rect(screen, BLACK, (cell[0] * CELL, cell[1] * CELL, CELL, CELL))
    for (c, r) in restricted_cells:
        pygame.draw.rect(screen, (255, 0, 0), (c * CELL, r * CELL, CELL, CELL)) 
    for zone in permanent_restricted_zones:
        for (c, r) in zone["cells"]:
            pygame.draw.rect(screen, (255, 140, 0), (c * CELL, r * CELL, CELL, CELL))    
    if len(path_px) > 1:
     pygame.draw.lines(screen, (200, 60, 60), False, path_px, 2)    

    # Draw the drone
    pygame.draw.circle(
        screen, BLUE, (drone_x, drone_y), 10
    )

    # Draw the destination
    pygame.draw.circle(
        screen, (0, 180, 0), goal_px, 12
    )

    pygame.display.update()

pygame.quit()   