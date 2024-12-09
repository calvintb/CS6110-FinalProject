from __future__ import annotations


class Intersection:
    def __init__(self, label=None, is_destination=False, is_source=False):
        self.label = label  
        self.connected_roads = [] # List of roads connected to this intersection
        self.is_destination = is_destination
        self.is_source = is_source

    def add_road(self, *roads):
        for road in roads:
            self.connected_roads.append(road)

    def get_connecting_roads(self):
        return self.connected_roads

    def __str__(self):
        return f"Intersection({self.label})"
    
    def __lt__(self, other):
        # Implement comparison logic. For simplicity, we compare by label here.
        if not isinstance(other, Intersection):
            return NotImplemented
        return self.label < other.label
