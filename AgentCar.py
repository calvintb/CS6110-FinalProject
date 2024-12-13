from __future__ import annotations

import random
from Car import Car
from Dijkstra import find_all_paths
from Intersection import Intersection

class AgentCar(Car):
    def __init__(self, start: Intersection, end: Intersection):
        super().__init__(start, end)
        self.explorability = .2

    def get_next_intersection(self) -> Intersection:
        if self.explorability > .05:
            self.explorability -= .01
        candidates: list[list[Intersection]] = [path for path in find_all_paths(self.current, self.end) if all(intersection not in self.path for intersection in path[1:])]
        candidates.sort(key=self.time_to_travel_potential_path)
        if random.random() < self.explorability:
            return random.choice(candidates)[1]
        return candidates[0][1]

    def time_to_travel_potential_path(self, path: list[Intersection]):
        time = 0
        for i in range(1, len(path)):
            road = path[i - 1].get_connecting_road(path[i])
            time += 3600 / self.road_memory.get(road, road.speed_limit)
        return time
