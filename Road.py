from __future__ import annotations

from Car import Car

class Road:

    def __init__(self, speed_limit: int, intersections: list[Intersection], length: float):
        self.speed_limit = speed_limit  # Base speed limit set at construction
        self.intersections = intersections  # Intersections this road connects
        self.traffic_count = 0  # Track number of cars currently on the road
        self.length = length  # Length of the road in kilometers

    def get_speed(self) -> float:
        """
        Calculate the effective speed on the road, adjusting for traffic congestion.
        The more cars on the road, the slower the speed, with a minimum speed cap.
        """
        congestion_factor = 5  # Speed reduction per car
        min_speed = 10  # Minimum speed limit, even under heavy traffic
        adjusted_speed = max(self.speed_limit - self.traffic_count * congestion_factor, min_speed)
        return adjusted_speed

    def get_connecting_intersections(self) -> list[Intersection]:
        """
        Get the list of intersections connected by this road.
        """
        return self.intersections

    def increment_traffic(self):
        """
        Increment the traffic count when a car uses the road.
        """
        self.traffic_count += 1

    def decrement_traffic(self):
        """
        Decrement the traffic count when a car leaves the road.
        """
        if self.traffic_count > 0:
            self.traffic_count -= 1

    def get_cost(self) -> float:
        """
        Calculate the cost of using this road, based on its length and traffic.
        The cost increases with traffic to simulate congestion.
        """
        base_cost = 1.0  # Base cost per kilometer
        traffic_cost = 0.5 * self.traffic_count  # Additional cost due to congestion
        return self.length * base_cost + traffic_cost

    def add_car(self, car: Car):
        """
        Add a car to the road, incrementing the traffic count.
        """
        self.increment_traffic()
        print(f"Car added to road {self}: Traffic count is now {self.traffic_count}")

    def remove_car(self, car: Car):
        """
        Remove a car from the road, decrementing the traffic count.
        """
        self.decrement_traffic()
        print(f"Car removed from road {self}: Traffic count is now {self.traffic_count}")

    def __str__(self):
        """
        Custom string representation for debugging.
        """
        return f"Road({self.speed_limit} km/h, Length: {self.length} km, Traffic: {self.traffic_count} cars)"
