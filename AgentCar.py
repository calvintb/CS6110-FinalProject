from __future__ import annotations

import random
from statistics import mean

from Car import Car
from Dijkstra import find_all_paths
from Intersection import Intersection

class AgentCar(Car):
    def __init__(self, start: Intersection, end: Intersection):
        super().__init__(start, end)

    def get_next_intersection(self) -> Intersection:
        candidates: list[list[Intersection]] = [path for path in find_all_paths(self.current, self.end) if all(intersection not in self.path for intersection in path[1:])]
        candidates.sort(key=self.time_to_travel_potential_path)
        if random.random() <= 0.1:
                return random.choice(candidates)[1]
        return candidates[0][1]
