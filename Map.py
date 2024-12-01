from __future__ import annotations

import heapq
import random
from AgentCar import PathType
from AgentCar import AgentCar
from Car import Car
from Intersection import Intersection
from Road import Road
from SimpleCar import SimpleCar
import matplotlib.pyplot as plt
import networkx as nx


def _next_intersection(intersection: Intersection, road: Road) -> Intersection:
    """
    Find the next intersection from a given intersection, based on the road.
    This method assumes the road connects two intersections.
    """

    connecting_intersections = road.get_connecting_intersections()

    for inter in connecting_intersections:

        if inter != intersection:
            return inter

    raise RuntimeError("Failed to find intersection attached to road")


class Map:
    __slots__ = 'width', 'height', 'intersections', 'roads', 'cars'

    def __init__(self, **kwargs):
        self.intersections = []  # List of all intersections in the map
        self.roads = []  # List of all roads in the map
        self.cars = []
        if "intersections" in kwargs:
            self.intersections = kwargs["intersections"]
        if "roads" in kwargs:
            self.roads = kwargs["roads"]
        if "cars" in kwargs:
            self.cars = kwargs["cars"]
        if len(self.roads) == 0 or len(self.intersections) == 0 or len(self.cars) == 0:
            print("Creating default map")
            self.__create_complex_map()
    
    def __create_complex_map(self):
        # Create intersections
        A = Intersection(label="A")
        B = Intersection(label="B")
        C = Intersection(label="C")
        D = Intersection(label="D")
        E = Intersection(label="E")
        F = Intersection(label="F")

        # Create roads
        AB = Road(speed_limit=50, length=10, intersections=[A, B])
        AF = Road(speed_limit=5, length=45, intersections=[A,F])
        AC = Road(speed_limit=40, length=15, intersections=[A, C])
        BD = Road(speed_limit=55, length=12, intersections=[B, D])
        CD = Road(speed_limit=35, length=10, intersections=[C, D])
        CE = Road(speed_limit=60, length=20, intersections=[C, E])
        DF = Road(speed_limit=50, length=18, intersections=[D, F])
        EF = Road(speed_limit=45, length=22, intersections=[E, F])

        # Add roads to intersections
        A.add_road(AB, AC, AF)
        B.add_road(AB, BD)
        C.add_road(AC, CD, CE)
        D.add_road(BD, CD, DF)
        E.add_road(CE, EF)
        F.add_road(DF, EF, AF)

        # Set up map
        self.intersections = [A, B, C, D, E, F]
        self.roads = [AB, AC, BD, CD, CE, DF, EF, AF]
        path_types = list(PathType) 
        for i in range(35):
            start = random.choice(self.intersections)
            end = random.choice([i for i in self.intersections if i != start])
            path_type = random.choice(path_types)  # Randomly select a path type
            car = AgentCar(path_type=path_type, start=start,end=end)
            self.cars.append(car)


    def __create_default_map(self):
        intersection1 = Intersection(label="A")
        intersection2 = Intersection(label="B")
        intersection3 = Intersection(label="C")

        road1 = Road(speed_limit=50, intersections=[intersection1, intersection2], length=12)
        road2 = Road(speed_limit=60, intersections=[intersection2, intersection3], length=13)

        intersection1.add_road(road1)
        intersection2.add_road(road1, road2)  
        intersection3.add_road(road2)

        self.cars = [SimpleCar(), SimpleCar(), SimpleCar(), SimpleCar(), SimpleCar()]
        self.intersections = [intersection1, intersection2, intersection3]
        self.roads = [road1, road2]


    def iterate(self):
        # Perform the iteration of the simulation (e.g., moving cars, updating state)
        print("Iterating simulation step.")

    def simulate(self):
        # Simulate the passage of time, car actions, etc.
        print("Simulating the environment.")

    def display_graph(self):
        print("Displaying map graph.")

    def find_least_intersections_path(self, start: Intersection, end: Intersection):
        """
        Finds the path with the least number of intersections (hops).
        """
        return self._find_path(start, end, weight_function=lambda road: 1)  # Each road adds 1 intersection to the path

    def find_shortest_path(self, start: Intersection, end: Intersection):
        """
        Considers the length of each path
        """
        return self._find_path(start, end, weight_function=lambda road: road.length)

    def find_cheapest_path(self, start: Intersection, end: Intersection):
        """
        Uses a road function to determine how much use is occurring on the road 
        """
        return self._find_path(start, end, weight_function=lambda road: road.get_cost())

    def find_shortest_time_path(self, start: Intersection, end: Intersection):
        """
        Looks for the fastest path
        """
        return self._find_path(start, end, weight_function=lambda road: road.length / road.get_speed())

    def find_highest_speed_limit_path(self, start: Intersection, end: Intersection):
        """
        Looks for the fastest speed limit allowed
        """
        return self._find_path(start, end, weight_function=lambda road: -road.speed_limit)  # Negative for max-heap logic

    def _find_path(self, start: Intersection, end: Intersection, weight_function):
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
                next_intersection = _next_intersection(current_intersection, road)
                if next_intersection not in visited:
                    total_weight = current_weight + weight_function(road)
                    heapq.heappush(priority_queue, (total_weight, next_intersection, path + [current_intersection]))

        raise RuntimeError("No path found between the intersections")
    
    def find_path_for_car(self, car: Car):
        if car.path_type == PathType.SHORTEST:
            path = self.find_shortest_path(car.start, car.end)
        elif car.path_type == PathType.CHEAPEST:
            path = self.find_cheapest_path(car.start, car.end)
        elif car.path_type == PathType.FASTEST:
            path = self.find_shortest_time_path(car.start, car.end)
        elif car.path_type == PathType.HIGHEST_SPEED:
            path = self.find_highest_speed_limit_path(car.start, car.end)
        else: path = self.find_least_intersections_path(car.start,car.end)

        # Add the car to each road in the path
        self.add_car_to_roads(car, path)
        car.path = path
        return path
    
    def add_car_to_roads(self, car: Car, path: list):
        for i in range(len(path) - 1):
            current_intersection = path[i]
            next_intersection = path[i + 1]

            road = self.find_road_between_intersections(current_intersection, next_intersection)
            if road:
                road.add_car(car)
                print(f"Car {car} added to road {road}")

    def find_road_between_intersections(self, intersection1: Intersection, intersection2: Intersection):
        for road in intersection1.get_connecting_roads():
            if intersection2 in road.get_connecting_intersections():
                return road
        return None
    
    def draw(self):
        G = nx.Graph()  # Create an empty graph

        # Add nodes (intersections) to the graph with labels
        for intersection in self.intersections:
            G.add_node(intersection.label)

        # Add edges (roads) between intersections
        for road in self.roads:
            intersection1, intersection2 = road.get_connecting_intersections()

            # Add edge with attributes for length and speed limit
            G.add_edge(
                intersection1.label, 
                intersection2.label, 
                length=road.length, 
                speed_limit=road.speed_limit,
                carsCount = road.traffic_count
            )

        # Draw the graph
        pos = nx.spring_layout(G)  # Positioning of nodes

        # Labels for intersections (nodes)
        node_labels = {intersection.label: intersection.label for intersection in self.intersections}
        nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=500, node_color="lightblue", font_size=10, font_weight="bold", font_color="black")

        # Labels for road attributes (edges)
        edge_labels = {}
        for u, v, data in G.edges(data=True):
            edge_labels[(u, v)] = f"Len: {data['length']}m, Speed: {data['speed_limit']} km/h, Cars: {data['carsCount']}"

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Map with Intersection and Road Information")
        plt.show()

    def draw_path(self, path: list[Intersection]):
        """
        Draws the map and highlights the path provided.

        :param path: A list of intersections forming the path to highlight.
        """
        G = nx.Graph()  # Create a new graph object for the map

        # Add nodes (intersections)
        for intersection in self.intersections:
            G.add_node(intersection, label=intersection.label)

        # Add edges (roads) between intersections
        for road in self.roads:
            inter1, inter2 = road.get_connecting_intersections()
            G.add_edge(inter1, inter2, weight=road.length, label=f"Speed: {road.speed_limit}, Length: {road.length}, Cars:{road.traffic_count}")

        # Create a list of edges that are part of the path
        path_edges = []
        for i in range(len(path) - 1):
            path_edges.append((path[i], path[i + 1]))

        # Draw the entire map
        pos = nx.spring_layout(G)  # Positions for nodes
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', edge_color='gray')

        # Highlight the path in a different color
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        # Draw edge labels (road info)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Draw node labels (intersection labels)
        node_labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_weight='bold')

        plt.title("Map with Highlighted Path")
        plt.show()

