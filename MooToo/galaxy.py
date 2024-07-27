""" Galaxy class"""

import io
import math
import random
import jsonpickle
from typing import TYPE_CHECKING, Optional
from MooToo.utils import (
    get_distance_tuple,
    get_distance,
    SystemId,
    PlanetId,
    ShipId,
    EmpireId,
    unique_empire_id,
    unique_ship_id,
    unique_system_id,
    unique_planet_id,
)
from MooToo.names import empire_names, empire_colours
from MooToo.empire import Empire, make_empire
from MooToo.system import System
from MooToo.constants import Technology, Building
from MooToo.ship import select_ship_type_by_name

if TYPE_CHECKING:
    from MooToo.system import System
    from MooToo.empire import Empire
    from MooToo.planet import Planet
    from MooToo.ship import Ship


NUM_SYSTEMS = 40
NUM_EMPIRES = 4
MAX_X = 530
MAX_Y = 420
MIN_DIST = 40  # Distance between systems


#####################################################################################################
class Galaxy:
    def __init__(self):
        self.systems: dict[SystemId, "System"] = {}
        self.empires: dict[EmpireId, Optional["Empire"]] = {}
        self.planets: dict[PlanetId, "Planet"] = {}
        self.ships: dict[ShipId, "Ship"] = {}
        self.turn_number = 0
        self.planet_num = 0
        self.unique = {
            "empire": unique_empire_id(),
            "ship": unique_ship_id(),
            "planet": unique_planet_id(),
            "system": unique_system_id(),
        }

    #################################################################################################
    def populate(self, tech: str = "avg"):
        """Fill the galaxy with things"""
        names = empire_names[:]
        colours = empire_colours[:]
        positions = get_system_positions(NUM_SYSTEMS)
        for _ in range(NUM_SYSTEMS):
            position = random.choice(positions)
            positions.remove(position)
            system = System(position, self)
            self.systems[system.id] = system
        for home_system in self.find_home_systems(NUM_EMPIRES):
            empire_name = pick_empire_name(names)
            colour = pick_colour(colours)
            empire = make_empire(empire_name, colour, home_system, self)
            self.empires[empire.id] = empire
            match tech:
                case "pre":
                    pre_start(empire, self)
                case "avg":
                    average_start(empire, self)
                case "adv":
                    advanced_start(empire, self)
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
    for _ in range(num_systems):
        while True:
            x = random.randrange(MIN_DIST, MAX_X - MIN_DIST)
            y = random.randrange(MIN_DIST, MAX_Y - MIN_DIST)
            for a, b in positions:  # Find a spot not too close to existing positions
                if get_distance(x, y, a, b) < MIN_DIST:
                    break
            else:
                positions.append((x, y))
                break
    return positions


#####################################################################################################
def pick_empire_name(names: list[str]):
    name = random.choice(names)
    names.remove(name)
    return name


#####################################################################################################
def pick_colour(colours: list[str]):
    colour = random.choice(colours)
    colours.remove(colour)

    return colour


#####################################################################################################
def save(galaxy: Galaxy, filename: str) -> None:
    file_name = f"{filename}_{galaxy.turn_number % 10}.json"
    with open(file_name, "w") as out_handle:
        out_handle.write(jsonpickle.encode(galaxy, keys=True, indent=2, warn=True))


#####################################################################################################
def load(file_handle: io.TextIOWrapper) -> Galaxy:
    return jsonpickle.loads(file_handle.read(), keys=True)


#####################################################################################################
def pre_start(empire: Empire, galaxy: Galaxy) -> None:
    """Start with pre-tech"""
    home_planet = list(empire.owned_planets)[0]

    home_planet.buildings.add(Building.MARINE_BARRACKS)
    home_planet.buildings.add(Building.STAR_BASE)
    empire.learnt(Technology.STAR_BASE)
    empire.learnt(Technology.MARINE_BARRACKS)
    empire.learnt(Technology.COLONY_BASE)


#####################################################################################################
def average_start(empire: Empire, galaxy: Galaxy) -> None:
    """Start with average tech"""
    home_system = empire.galaxy.systems[list(empire.known_systems)[0]]
    pre_start(empire, galaxy)
    empire.learnt(Technology.STANDARD_FUEL_CELLS)
    empire.learnt(Technology.NUCLEAR_DRIVE)
    empire.learnt(Technology.COLONY_SHIP)
    empire.learnt(Technology.OUTPOST_SHIP)
    empire.learnt(Technology.TRANSPORT)

    empire.add_ship(ship=select_ship_type_by_name("Frigate", galaxy), system=home_system)
    empire.add_ship(ship=select_ship_type_by_name("Frigate", galaxy), system=home_system)
    empire.add_ship(ship=select_ship_type_by_name("ColonyShip", galaxy), system=home_system)


#####################################################################################################
def advanced_start(empire: Empire, galaxy: Galaxy) -> None:
    """Start with advanced tech"""
    average_start(empire, galaxy)
    # Do more stuff


# EOF
