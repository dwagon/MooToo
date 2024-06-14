""" Galaxy class"""

import math
import random
import jsonpickle

from MooToo import get_distance, get_distance_tuple, empire_names, StarColour
from MooToo.system import System
from MooToo.empire import Empire
from MooToo.planet import make_home_planet

NUM_SYSTEMS = 40
NUM_EMPIRES = 4
MAX_X = 530
MAX_Y = 420


#####################################################################################################
#####################################################################################################
class Galaxy:
    def __init__(self):
        self.systems: dict[int, "System"] = {}
        self.empires: dict[str, "Empire"] = {}
        self.turn_number = 0

    #####################################################################################################
    def populate(self):
        """Fill the galaxy with things"""
        positions = self.get_system_positions()
        for _id, _ in enumerate(range(NUM_SYSTEMS)):
            position = random.choice(positions)
            positions.remove(position)
            self.systems[_id] = System(_id, position)
        for home_system in self.find_home_systems():
            empire_name = random.choice(empire_names)
            empire_names.remove(empire_name)
            self.make_empire(empire_name, home_system)
        for system in self.systems.values():
            system.make_orbits()

    #####################################################################################################
    def find_home_systems(self) -> list["System"]:
        """Find suitable planets for home planets"""
        # Create an arc around the galaxy and put home planets evenly spaced around that arc
        home_systems = []
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
            for system in self.systems.values():
                distance = get_distance_tuple(position, system.position)
                if distance < min_dist:
                    min_dist = distance
                    min_system = system
            home_systems.append(min_system)
        return home_systems

    #####################################################################################################
    def turn(self):
        """End of turn"""
        self.turn_number += 1
        for empire in self.empires.values():
            empire.turn()

    #####################################################################################################
    def make_empire(self, empire_name: str, home_system: "System"):
        """ """
        home_system.colour = StarColour.YELLOW
        empire = Empire(empire_name, self)
        self.empires[empire_name] = empire
        home_planet = make_home_planet(home_system)
        empire.set_home_planet(home_planet)
        home_system.orbits.append(home_planet)
        random.shuffle(home_system.orbits)

    #####################################################################################################
    def get_system_positions(self) -> list[tuple[int, int]]:
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
def save(galaxy: Galaxy, filename: str) -> None:
    fname = f"{filename}_{galaxy.turn_number % 10}.json"
    print(f"Saving as {fname}")
    with open(fname, "w") as outfh:
        outfh.write(jsonpickle.encode(galaxy, indent=2))


#####################################################################################################
def load(filename: str) -> Galaxy:
    with open(filename) as infh:
        galaxy = jsonpickle.loads(infh.read())
    return galaxy


# EOF
