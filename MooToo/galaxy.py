""" Galaxy class"""

import math
import random

from MooToo.system import System, StarColour
from MooToo.empire import Empire
from MooToo.names import empire_names


#####################################################################################################
#####################################################################################################
class Galaxy:
    def __init__(self, config):
        self.config = config
        self.systems = {}
        self.empires = {}
        self.turn_number = 0

    #####################################################################################################
    def populate(self):
        """Fill the galaxy with things"""
        positions = self.get_positions()
        for _ in range(self.config["galaxy"]["num_systems"]):
            position = random.choice(positions)
            positions.remove(position)
            self.systems[position] = System(position, self.config)
        for home_system in self.find_home_systems():
            self.make_empire(home_system)
        for system in self.systems.values():
            system.make_orbits()

    #####################################################################################################
    def find_home_systems(self) -> list[System]:
        """Find suitable planets for home planets"""
        # Create an arc around the galaxy and put home planets evenly spaced around that arc
        home_planets = []
        arc_distance = int(360 / self.config["empires"]["number"])
        radius = min(self.config["galaxy"]["max_x"], self.config["galaxy"]["max_y"]) * 0.75 / 2
        for degree in range(0, 359, arc_distance):
            angle = math.radians(degree)
            position = (
                radius * math.cos(angle) + self.config["galaxy"]["max_x"] / 2,
                radius * math.sin(angle) + self.config["galaxy"]["max_y"] / 2,
            )
            # Find the system closest to this point
            min_dist = 999999
            min_system = None
            for sys_position, system in self.systems.items():
                distance = get_distance(position[0], position[1], sys_position[0], sys_position[1])
                if distance < min_dist:
                    min_dist = distance
                    min_system = system
            home_planets.append(min_system)
        return home_planets

    #####################################################################################################
    def turn(self):
        """End of turn"""
        self.turn_number += 1
        for system in self.systems.values():
            system.turn()

    #####################################################################################################
    def make_empire(self, home_system: System):
        """ """
        name = random.choice(empire_names)
        empire_names.remove(name)
        home_system.colour = StarColour.YELLOW
        self.empires[name] = Empire(name, home_system, self.config)
        home_system.orbits[3] = self.empires[name].make_home_planet(3)

    #####################################################################################################
    def get_positions(self) -> list[tuple[int, int]]:
        """Return suitable positions"""
        positions = []
        min_dist = 30
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


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


# EOF
