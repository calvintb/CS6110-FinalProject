from __future__ import annotations
import matplotlib.pyplot as plt
import networkx as nx

from Car import Car
from Intersection import Intersection
from Road import Road

from DijkstraCar import DijkstraCar, PathType
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
            self.__create_complex_map()
    
    def __create_complex_map(self):
        A = Intersection(label="A")
        B = Intersection(label="B")
        C = Intersection(label="C")
        D = Intersection(label="D")
        E = Intersection(label="E")
        F = Intersection(label="F")
        G = Intersection(label="G")
        H = Intersection(label="H")

        # Create roads
        AB = Road(speed_limit=15, label="AB")
        AC = Road(speed_limit=40, label="AC")
        AD = Road(speed_limit=40, label="AD")
        BE = Road(speed_limit=30, label="BE")
        BF = Road(speed_limit=55, label="BF")
        BG = Road(speed_limit=55, label="BG")
        CE = Road(speed_limit=35, label="CE")
        CF = Road(speed_limit=60, label="CF")
        CG = Road(speed_limit=50, label="CG")
        DE = Road(speed_limit=50, label="DE")
        DF = Road(speed_limit=50, label="DF")
        DG = Road(speed_limit=50, label="DG")
        EH = Road(speed_limit=45, label="EH")
        FH = Road(speed_limit=45, label="FH")
        GH = Road(speed_limit=45, label="GH")

        # Add roads to intersections
        A.add_road((AB, B), (AC, C), (AD, D))
        B.add_road((AB, A), (BE, E), (BF, F), (BG, G))
        C.add_road((AC, A), (CE, E), (CF, F), (CG, G))
        D.add_road((AD, A), (DE, E), (DF, F), (DG, G))
        E.add_road((BE, B), (CE, C), (DE, D), (EH, H))
        F.add_road((BF, B), (CF, C), (DF, D), (FH, H))
        G.add_road((BG, B), (CG, C), (DG, D), (GH, H))
        H.add_road((EH, E), (FH, F), (GH, G))

        self.cars = []
        for _ in range(500):
            self.cars.append(DijkstraCar(A, H, PathType.FASTEST))
        self.intersections = [A, B, C, D, E, F, G, H]
        self.roads = [AB, AC, AD, BE, BF, BG, CE, CF, CG, DE, DF, DG, EH, FH, GH]


    def __create_default_map(self):
        A = Intersection(label="A")
        B = Intersection(label="B")
        C = Intersection(label="C")
        D = Intersection(label="D")
        E = Intersection(label="E")
        F = Intersection(label="F")
        G = Intersection(label="G")
        H = Intersection(label="H")

        # Create roads
        AB = Road(speed_limit=15, label="AB")
        AC = Road(speed_limit=40, label="AC")
        AD = Road(speed_limit=40, label="AD")
        BE = Road(speed_limit=30, label="BE")
        BF = Road(speed_limit=55, label="BF")
        BG = Road(speed_limit=55, label="BG")
        CE = Road(speed_limit=35, label="CE")
        CF = Road(speed_limit=60, label="CF")
        CG = Road(speed_limit=50, label="CG")
        DE = Road(speed_limit=50, label="DE")
        DF = Road(speed_limit=30, label="DF")
        DG = Road(speed_limit=80, label="DG")
        EH = Road(speed_limit=45, label="EH")
        FH = Road(speed_limit=45, label="FH")
        GH = Road(speed_limit=45, label="GH")

        # Add roads to intersections
        A.add_road((AB, B), (AC, C), (AD, D))
        B.add_road((AB, A), (BE, E), (BF, F), (BG, G))
        C.add_road((AC, A), (CE, E), (CF, F), (CG, G))
        D.add_road((AD, A), (DE, E), (DF, F), (DG, G))
        E.add_road((BE, B), (CE, C), (DE, D), (EH, H))
        F.add_road((BF, B), (CF, C), (DF, D), (FH, H))
        G.add_road((BG, B), (CG, C), (DG, D), (GH, H))
        H.add_road((EH, E), (FH, F), (GH, G))

        self.cars = []
        for _ in range(500):
            self.cars.append(AgentCar(A, H))
        self.intersections = [A, B, C, D, E, F, G, H]
        self.roads = [AB, AC, AD, BE, BF, BG, CE, CF, CG, DE, DF, DG, EH, FH, GH]

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

    def simulate(self):
        self.iterate()
        simulations = 0
        while not self.at_nash_equilibrium() and simulations < 100:
            self.reset()
            self.iterate()
            simulations += 1
            if simulations == 1 or simulations == 10 or simulations == 20 or simulations == 50:
                self.draw()

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
                    speed=round(road.get_speed(), 2),
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
