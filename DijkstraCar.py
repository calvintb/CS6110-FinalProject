from __future__ import annotations
from Car import Car
from Intersection import Intersection
from Road import Road
import heapq
from enum import Enum

class PathType(Enum):
    SHORTEST = 1
    CHEAPEST = 2
    FASTEST = 3
    HIGHEST_SPEED = 4
    LEAST_INTERSECTIONS = 5

class AgentCar(Car):

    def __init__(self, start:Intersection, end: Intersection, path_type:PathType= PathType.FASTEST):
        self.path_type = path_type 
        super().__init__(start=start, end=end)

    def take_action(self):
        if self.is_at_end():
            return
        path = self.find_path_for_car()
        next_intersection: Intersection = path[1]
        next_road = self.current.get_connecting_road(next_intersection)
        next_road.add_car(self)
        next_intersection = next_road.get_other_intersection(self.current)
        self.current = next_intersection

    def __find_path(self, start: Intersection, end: Intersection, weight_function):
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
                next_intersection = road.get_other_intersection(current_intersection)
                if next_intersection not in visited:
                    total_weight = current_weight + weight_function(road)
                    heapq.heappush(priority_queue, (total_weight, next_intersection, path + [current_intersection]))

        raise RuntimeError("No path found between the intersections")

    def find_least_intersections_path(self, start: Intersection, end: Intersection):
        """
        Finds the path with the least number of intersections (hops).
        """
        return self.__find_path(start, end, weight_function=lambda road: 1)  # Each road adds 1 intersection to the path

    def find_shortest_path(self, start: Intersection, end: Intersection):
        """
        Considers the length of each path
        """
        return self.__find_path(start, end, weight_function=lambda road: road.length)

    def find_cheapest_path(self, start: Intersection, end: Intersection):
        """
        Uses a road function to determine how much use is occurring on the road
        """
        return self.__find_path(start, end, weight_function=lambda road: road.get_cost())

    def find_shortest_time_path(self, start: Intersection, end: Intersection):
        """
        Looks for the fastest path
        """
        return self.__find_path(start, end, weight_function=lambda road: road.length / road.get_speed())

    def find_highest_speed_limit_path(self, start: Intersection, end: Intersection):
        """
        Looks for the fastest speed limit allowed
        """
        return self.__find_path(start, end, weight_function=lambda road: road.speed_limit)

    def find_path_for_car(self):
        if self.path_type == PathType.SHORTEST:
            path = self.find_shortest_path(self.current, self.end)
        elif self.path_type == PathType.CHEAPEST:
            path = self.find_cheapest_path(self.current, self.end)
        elif self.path_type == PathType.FASTEST:
            path = self.find_shortest_time_path(self.current, self.end)
        elif self.path_type == PathType.HIGHEST_SPEED:
            path = self.find_highest_speed_limit_path(self.current, self.end)
        else:
            path = self.find_least_intersections_path(self.current, self.end)
        return path
