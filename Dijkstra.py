from __future__ import annotations
import heapq
from Intersection import Intersection

def __dijkstra_find_path(start: Intersection, end: Intersection, weight_function):
    # Priority queue for Dijkstra's algorithm
    priority_queue = []
    heapq.heappush(priority_queue, (0, start, []))  # (cumulative weight, current intersection, path taken)
    visited = set()

    while priority_queue:
        current_weight, current_intersection, path = heapq.heappop(priority_queue)

        if current_intersection in visited:
            continue
        visited.add(current_intersection)

        # Check if we've reached the destination
        if current_intersection == end:
            return path + [current_intersection]

        # Explore connecting roads
        for road in current_intersection.get_connecting_roads():
            next_intersection = current_intersection.get_connecting_intersection(road)
            if next_intersection not in visited:
                total_weight = current_weight + weight_function(road)
                heapq.heappush(priority_queue, (total_weight, next_intersection, path + [current_intersection]))

    raise RuntimeError("No path found between the intersections")

def find_all_paths(start: Intersection, end: Intersection, path: list[Intersection]=[]):
    """Finds all paths from start to end in a given graph."""
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in start.get_connecting_intersections():
        if node not in path:
            new_paths = find_all_paths(node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

def find_least_intersections_path(start: Intersection, end: Intersection):
    """
    Finds the path with the least number of intersections (hops).
    """
    return __dijkstra_find_path(start, end, weight_function=lambda road: 1)  # Each road adds 1 intersection to the path

def find_shortest_path(start: Intersection, end: Intersection):
    """
    Considers the length of each path
    """
    return __dijkstra_find_path(start, end, weight_function=lambda road: road.length)

def find_cheapest_path(start: Intersection, end: Intersection):
    """
    Uses a road function to determine how much use is occurring on the road
    """
    return __dijkstra_find_path(start, end, weight_function=lambda road: road.get_cost())

def find_shortest_time_path(start: Intersection, end: Intersection):
    """
    Looks for the fastest path
    """
    return __dijkstra_find_path(start, end, weight_function=lambda road: road.length / road.get_speed())

def find_highest_speed_limit_path(start: Intersection, end: Intersection):
    """
    Looks for the fastest speed limit allowed
    """
    return __dijkstra_find_path(start, end, weight_function=lambda road: road.speed_limit)
