from __future__ import annotations
from Map import Map




if __name__ == "__main__":
    my_map = Map()
    my_map.draw()

    for car in my_map.cars:
        my_map.find_path_for_car(car=car)
    my_map.draw()
