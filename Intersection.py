from __future__ import annotations
from Road import Road

class Intersection:
    def __init__(self, label=None):
        self.label = label  
        self.connections: list[tuple[Road, Intersection]] = [] # List of roads connected to this intersection

    def add_road(self, *connections: tuple[Road, Intersection]):
        for connection in connections:
            self.connections.append(connection)

    def get_connecting_roads(self):
        return [x[0] for x in self.connections]

    def get_connecting_intersections(self):
        return [x[1] for x in self.connections]

    def get_connecting_road(self, other: Intersection):
        if self is other:
            raise RuntimeError("Cannot find a connecting road between two identical intersections")
        candidates = [x[0] for x in self.connections if other is x[1]]
        if len(candidates) == 0:
            raise RuntimeError(f"Failed to find a road that connects {self} and {other}")
        elif len(candidates) > 1:
            raise RuntimeError(f"Found multiple roads that connect {self} and {other}")
        return candidates[0]

    def get_connecting_intersection(self, road: Road) -> Intersection:
        if road not in self.get_connecting_roads():
            raise RuntimeError(f"This road {road} is not connected to this intersection {self}")

        candidates = [x[1] for x in self.connections if road is x[0]]
        if len(candidates) == 0:
            raise RuntimeError(f"Failed to find an intersection from {self} and {road}")
        elif len(candidates) > 1:
            raise RuntimeError(f"Found multiple intersections from {self} and {road}")
        return candidates[0]


    def __str__(self):
        return f"Intersection({self.label})"
    
    def __lt__(self, other):
        # Implement comparison logic. For simplicity, we compare by label here.
        if not isinstance(other, Intersection):
            return NotImplemented
        return self.label < other.label
