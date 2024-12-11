from __future__ import annotations
from abc import ABC, abstractmethod
from Intersection import Intersection
from Road import Road

class Car(ABC):
    __slots__ = 'road_memory', 'current', 'start', 'end', 'path', 'id'
    car_id = 0

    def __init__(self, start: Intersection, end: Intersection):
        self.road_memory: dict[Road, float] = {}
        self.start = start
        self.current = start
        self.end = end
        self.path = [start]
        Car.car_id += 1
        self.id = Car.car_id

    @abstractmethod
    def get_next_intersection(self) -> Intersection:
        pass

    def take_action(self) -> None:
        """
        The car takes action based on its current state and the available roads at the intersection.
        Returns a road to travel to the next intersection.
        """
        if self.is_at_end():
            return
        next_intersection = self.get_next_intersection()
        next_road = next_intersection.get_connecting_road(self.current)
        next_road.add_car()  # Car chooses this road, so we increment traffic
        self.current = next_intersection
        self.path.append(next_intersection)

    def learn(self):
        """
        The car learns about available roads, possibly improving decision-making in the future.
        """
        for road in self.get_road_path():
            if road in self.road_memory:
                self.road_memory[road] = (self.road_memory[road] + road.get_speed()) / 2
            else:
                self.road_memory[road] = road.get_speed()

    def get_road_path(self):
        roads = []
        for i in range(1, len(self.path)):
            roads.append(self.path[i-1].get_connecting_road(self.path[i]))

        return roads

    def reset(self):
        self.current = self.start
        self.path = [self.start]

    def is_at_end(self):
        return self.current is self.end

    def time_to_travel_path(self):
        return self.time_to_travel_potential_path(self.path)

    def time_to_travel_potential_path(self, path: list[Intersection]):
        time = 0
        for i in range(1, len(path)):
            time += 100 / path[i-1].get_connecting_road(path[i]).get_speed()
        return time

    def __str__(self):
        return f"Car({self.id})"

