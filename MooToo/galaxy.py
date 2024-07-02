""" Galaxy class"""

import io
import math
import random
import jsonpickle
from MooToo.utils import get_distance_tuple, get_distance
from MooToo.names import empire_names
from MooToo.empire import Empire, make_empire
from MooToo.system import System
from MooToo.constants import Technology
from MooToo.ship import select_ship_type_by_name

NUM_SYSTEMS = 40
NUM_EMPIRES = 4
MAX_X = 530
MAX_Y = 420


#####################################################################################################
class Galaxy:
    def __init__(self):
        self.systems: dict[int, "System"] = {}
        self.empires: dict[str, "Empire"] = {}
        self.turn_number = 0

    #################################################################################################
    def populate(self, tech: str = "avg"):
        """Fill the galaxy with things"""
        positions = get_system_positions(NUM_SYSTEMS)
        for _id in range(NUM_SYSTEMS):
            position = random.choice(positions)
            positions.remove(position)
            self.systems[_id] = System(_id, position, self)
        for home_system in self.find_home_systems(NUM_EMPIRES):
            empire_name = random.choice(empire_names)
            empire_names.remove(empire_name)
            empire = make_empire(empire_name, home_system)
            self.empires[empire_name] = empire
            match tech:
                case "pre":
                    pre_start(empire, home_system)
                case "avg":
                    average_start(empire, home_system)
                case "adv":
                    advanced_start(empire, home_system)
        for system in self.systems.values():
            system.make_orbits()

    #####################################################################################################
    def turn(self):
        """End of turn"""
        self.turn_number += 1
        for system in self.systems.values():
            system.turn()
        for empire in self.empires.values():
            empire.turn()

    #####################################################################################################
    def find_home_systems(self, num_empires: int) -> list["System"]:
        """Find suitable planets for home planets"""
        # Create an arc around the galaxy and put home planets evenly spaced around that arc
        home_systems = []
        arc_distance = 360 // num_empires
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
def get_system_positions(num_systems: int) -> list[tuple[int, int]]:
    """Return suitable positions"""
    positions = []
    min_dist = 30
    for _ in range(num_systems):
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
    file_name = f"{filename}_{galaxy.turn_number % 10}.json"
    with open(file_name, "w") as out_handle:
        out_handle.write(jsonpickle.encode(galaxy, keys=True, indent=2, warn=True))


#####################################################################################################
def load(file_handle: io.TextIOWrapper) -> Galaxy:
    return jsonpickle.loads(file_handle.read(), keys=True)


#####################################################################################################
def pre_start(empire: Empire, home_system: System) -> None:
    """Start with pre-tech"""
    pass


#####################################################################################################
def average_start(empire: Empire, home_system: System) -> None:
    """Start with average tech"""
    empire.learnt(Technology.STANDARD_FUEL_CELLS)
    empire.learnt(Technology.NUCLEAR_DRIVE)
    empire.learnt(Technology.COLONY_SHIP)
    empire.learnt(Technology.OUTPOST_SHIP)
    empire.learnt(Technology.TRANSPORT)

    empire.add_ship(ship=select_ship_type_by_name("Frigate"), system=home_system)
    empire.add_ship(ship=select_ship_type_by_name("Frigate"), system=home_system)
    empire.add_ship(ship=select_ship_type_by_name("ColonyShip"), system=home_system)


#####################################################################################################
def advanced_start(empire: Empire, home_system: System) -> None:
    """Start with advanced tech"""
    average_start(empire, home_system)
    # Do more stuff


# EOF
