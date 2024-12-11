from __future__ import annotations

from Car import Car
from enum import Enum
from Dijkstra import *

class PathType(Enum):
    SHORTEST = 1
    FASTEST = 2
    HIGHEST_SPEED = 3
    LEAST_INTERSECTIONS = 4

class DijkstraCar(Car):
    def __init__(self, start: Intersection, end: Intersection, path_type:PathType= PathType.FASTEST):
        self.path_type = path_type 
        super().__init__(start=start, end=end)

    def get_next_intersection(self) -> Intersection:
        return self.find_path_for_car()[1]

    def find_path_for_car(self):
        if self.path_type == PathType.SHORTEST:
            path = find_shortest_path(self.current, self.end)
        elif self.path_type == PathType.FASTEST:
            path = find_shortest_time_path(self.current, self.end)
        elif self.path_type == PathType.HIGHEST_SPEED:
            path = find_highest_speed_limit_path(self.current, self.end)
        else:
            path = find_least_intersections_path(self.current, self.end)
        return path
