""" Galaxy class"""

import glob
import importlib
import math
import os
import random

from MooToo.system import System, StarColour
from MooToo.empire import Empire
from MooToo.planetbuilding import PlanetBuilding
from MooToo.research import Research
from MooToo.names import empire_names

NUM_SYSTEMS = 40
NUM_EMPIRES = 4
MAX_X = 530
MAX_Y = 420


#####################################################################################################
#####################################################################################################
class Galaxy:
    def __init__(self):
        self.systems: dict[tuple[int, int], System] = {}
        self.empires: dict[str, Empire] = {}
        self.buildings: dict[str, PlanetBuilding] = load_buildings()  # Buildings are stateless, so one per game
        self.researches: dict[str, Research] = load_researches()
        self.turn_number = 0

    #####################################################################################################
    def populate(self):
        """Fill the galaxy with things"""
        positions = self.get_positions()
        for _ in range(NUM_SYSTEMS):
            position = random.choice(positions)
            positions.remove(position)
            self.systems[position] = System(position, self)
        for home_system in self.find_home_systems():
            self.make_empire(home_system)
        for system in self.systems.values():
            system.make_orbits()

    #####################################################################################################
    def find_home_systems(self) -> list[System]:
        """Find suitable planets for home planets"""
        # Create an arc around the galaxy and put home planets evenly spaced around that arc
        home_planets = []
        arc_distance = int(360 / NUM_EMPIRES)
        radius = min(MAX_X, MAX_Y) * 0.75 / 2
        for degree in range(0, 359, arc_distance):
            angle = math.radians(degree)
            position = (
                radius * math.cos(angle) + MAX_X / 2,
                radius * math.sin(angle) + MAX_Y / 2,
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
        for empire in self.empires.values():
            empire.turn()

    #####################################################################################################
    def make_empire(self, home_system: System):
        """ """
        name = random.choice(empire_names)
        empire_names.remove(name)
        home_system.colour = StarColour.YELLOW
        self.empires[name] = Empire(name, home_system, self)
        home_system.orbits[3] = self.empires[name].make_home_planet(3, home_system)
        self.empires[name].know_system(home_system)

    #####################################################################################################
    def get_positions(self) -> list[tuple[int, int]]:
        """Return suitable positions"""
        positions = []
        min_dist = 30
        num_objects = NUM_SYSTEMS
        for _ in range(num_objects):
            while True:
                x = random.randrange(min_dist, MAX_X - min_dist)
                y = random.randrange(min_dist, MAX_Y - min_dist)
                for a, b in positions:  # Find a spot not too close to existing positions
                    if get_distance(x, y, a, b) < min_dist:
                        break
                else:
                    positions.append((x, y))
                    break
        return positions


#####################################################################################################
def load_buildings() -> dict[str, PlanetBuilding]:
    path = "MooToo/buildings"
    mapping: dict[str, PlanetBuilding] = {}
    files = glob.glob(f"{path}/*.py")
    for file_name in [os.path.basename(_) for _ in files]:
        file_name = file_name.replace(".py", "")
        mod = importlib.import_module(f"{path.replace('/', '.')}.{file_name}")
        classes = dir(mod)
        for kls in classes:
            if kls.startswith("Building"):
                klass = getattr(mod, kls)
                mapping[klass().name] = klass()
                break
    return mapping


#####################################################################################################
def load_researches() -> dict[str, Research]:
    path = "MooToo/researches"
    mapping: dict[str, Research] = {}
    files = glob.glob(f"{path}/*.py")
    for file_name in [os.path.basename(_) for _ in files]:
        file_name = file_name.replace(".py", "")
        mod = importlib.import_module(f"{path.replace('/', '.')}.{file_name}")
        classes = dir(mod)
        for kls in classes:
            if kls.startswith("Research") and kls != "Research":
                klass = getattr(mod, kls)
                if issubclass(klass, Research):
                    mapping[klass().name] = klass()
    return mapping


#####################################################################################################
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# EOF
