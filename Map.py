from __future__ import annotations
import random
import matplotlib.pyplot as plt
import networkx as nx

from Car import Car
from Intersection import Intersection
from Road import Road

from DijkstraCar import DijkstraCar, PathType
from SimpleCar import SimpleCar
from AgentCar import AgentCar



class Map:
    __slots__ = 'width', 'height', 'intersections', 'roads', 'cars'

    def __init__(self, **kwargs):
        self.intersections: list[Intersection] = []  # List of all intersections in the map
        self.roads: list[Road] = []  # List of all roads in the map
        self.cars: list[Car] = []
        if "intersections" in kwargs:
            self.intersections: list[Intersection] = kwargs["intersections"]
        if "roads" in kwargs:
            self.roads: list[Road] = kwargs["roads"]
        if "cars" in kwargs:
            self.cars: list[Car] = kwargs["cars"]
        if len(self.roads) == 0 or len(self.intersections) == 0 or len(self.cars) == 0:
            print("Creating default map")
            self.__create_default_map()
    
    def __create_complex_map(self):
        # Create intersections
        A = Intersection(label="A")
        B = Intersection(label="B")
        C = Intersection(label="C")
        D = Intersection(label="D")
        E = Intersection(label="E")
        F = Intersection(label="F")

        # Create roads
        AB = Road(speed_limit=50, length=10)
        AF = Road(speed_limit=5, length=45)
        AC = Road(speed_limit=40, length=15)
        BD = Road(speed_limit=55, length=12)
        CD = Road(speed_limit=35, length=10)
        CE = Road(speed_limit=60, length=20)
        DF = Road(speed_limit=50, length=18)
        EF = Road(speed_limit=45, length=22)

        # Add roads to intersections
        A.add_road((AB, B), (AC, C))
        B.add_road((AB, A), (BD, D))
        C.add_road((AC, A), (CD, D), (CE, E))
        D.add_road((BD, B), (CD, C), (DF, F))
        E.add_road((CE, C), (EF, F))
        F.add_road((DF, D), (EF, E))

        # Set up map
        self.intersections = [A, B, C, D, E, F]
        self.roads = [AB, AC, BD, CD, CE, DF, EF, AF]
        path_types = list(PathType) 
        for i in range(35):
            start = random.choice(self.intersections)
            end = random.choice([i for i in self.intersections if i != start])
            path_type = random.choice(path_types)  # Randomly select a path type
            car = DijkstraCar(path_type=path_type, start=start, end=end)
            self.cars.append(car)


    def __create_default_map(self):
        A = Intersection(label="A")
        B = Intersection(label="B")
        C = Intersection(label="C")
        D = Intersection(label="D")
        E = Intersection(label="E")
        F = Intersection(label="F")

        # Create roads
        AB = Road(speed_limit=50, label="AB")
        AC = Road(speed_limit=40, label="AC")
        BC = Road(speed_limit=30, label="BC")
        BD = Road(speed_limit=55, label="BD")
        CD = Road(speed_limit=35, label="CD")
        CE = Road(speed_limit=60, label="CE")
        DF = Road(speed_limit=50, label="DF")
        EF = Road(speed_limit=45, label="EF")

        # Add roads to intersections
        A.add_road((AB, B), (AC, C))
        B.add_road((AB, A), (BC, C), (BD, D))
        C.add_road((AC, A), (BC, B), (CD, D), (CE, E))
        D.add_road((BD, B), (CD, C), (DF, F))
        E.add_road((CE, C), (EF, F))
        F.add_road((DF, D), (EF, E))

        self.cars = []
        for _ in range(500):
            self.cars.append(AgentCar(A, F))
        self.intersections = [A, B, C, D, E, F]
        self.roads = [AB, AC, BC, BD, CD, CE, DF, EF]

    def reset(self):
        for road in self.roads:
            road.reset_traffic()
        for car in self.cars:
            car.reset()

    def have_all_cars_finished(self) -> bool:
        return all([x.is_at_end() for x in self.cars])

    def at_nash_equilibrium(self):
        mean_travel_time = sum(map(lambda car: car.time_to_travel_path(), self.cars)) / len(self.cars)
        allowed_threshold = 1
        threshold = 0
        for car in self.cars:
            threshold = max(abs(car.time_to_travel_path() - mean_travel_time), threshold)
        return threshold <= allowed_threshold

    def iterate(self):
        iterations = 0
        while not self.have_all_cars_finished():
            for car in self.cars:
                car.take_action()
            iterations += 1
        for car in self.cars:
            car.learn()
        print(f"It took {iterations} iterations for all cars to reach their destination.")

    def simulate(self):
        self.iterate()
        while not self.at_nash_equilibrium():
        # for _ in range(500):
            self.reset()
            self.iterate()
        print()

    def draw(self):
        G = nx.Graph()  # Create an empty graph

        # Add nodes (intersections) to the graph with labels
        for intersection in self.intersections:
            G.add_node(intersection.label)

        # Add edges (roads) between intersections
        for inter1 in self.intersections:
            for inter2 in inter1.get_connecting_intersections():
                road = inter1.get_connecting_road(inter2)

                # Add edge with attributes for length and speed limit
                G.add_edge(
                    inter1.label,
                    inter2.label,
                    speed=road.get_speed(),
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
            edge_labels[(u, v)] = f"Speed: {data['speed']} km/h, Cars: {data['carsCount']}"

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
        for inter1 in self.intersections:
            for inter2 in inter1.get_connecting_intersections():
                road = inter1.get_connecting_road(inter2)
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

