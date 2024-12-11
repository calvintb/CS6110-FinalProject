from __future__ import annotations
import random
from Car import Car
from Intersection import Intersection
from Dijkstra import find_all_paths

class SimpleCar(Car):
    def __init__(self, start: Intersection, end: Intersection):
        super().__init__(start, end)

    def get_next_intersection(self) -> Intersection:
        return random.choice(find_all_paths(self.current, self.end))[1]
