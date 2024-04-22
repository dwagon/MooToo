""" Galaxy class"""

import math
import random

from MooToo.system import System


class Galaxy:
    def __init__(self, config):
        self.config = config
        self.systems = {}

    def populate(self):
        """Fill the galaxy with things"""
        positions = self.get_positions()
        for _ in range(self.config["galaxy"]["num_systems"]):
            position = random.choice(positions)
            positions.remove(position)
            self.systems[position] = System(position, self.config)

    def get_positions(self) -> list[tuple[int, int]]:
        """Return suitable positions"""
        positions = []
        min_dist = 40
        num_objects = self.config["galaxy"]["num_systems"]
        for _ in range(num_objects):
            while True:
                x = random.randrange(min_dist, self.config["galaxy"]["max_x"] - min_dist)
                y = random.randrange(min_dist, self.config["galaxy"]["max_y"] - min_dist)
                for a, b in positions:
                    if get_distance(x, y, a, b) < min_dist:
                        break
                else:
                    positions.append((x, y))
                    break
        return positions


def get_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


# EOF
