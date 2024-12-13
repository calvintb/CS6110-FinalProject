from __future__ import annotations

class Road:
    def __init__(self, speed_limit: int, label: str):
        self.speed_limit = speed_limit  # Base speed limit set at construction
        self.traffic_count = 0  # Track number of cars currently on the road
        self.label = label

    def get_speed(self) -> float:
        """
        Calculate the effective speed on the road, adjusting for traffic congestion.
        The more cars on the road, the slower the speed, with a minimum speed cap.
        """
        congestion_factor = .1 # Speed reduction per car
        min_speed = 2  # Minimum speed limit, even under heavy traffic
        adjusted_speed = max(self.speed_limit - self.traffic_count * congestion_factor, min_speed)
        return adjusted_speed

    def reset_traffic(self):
        self.traffic_count = 0

    def add_car(self):
        """
        Add a car to the road, incrementing the traffic count.
        """
        self.traffic_count += 1

    def __str__(self):
        """
        Custom string representation for debugging.
        """
        return f"Road{self.label}({self.get_speed():.2f} km/h)"
