""" Galaxy class"""

import math
import random
import jsonpickle
from typing import TYPE_CHECKING
from MooToo.planet import make_home_planet
from MooToo.utils import get_distance_tuple, get_distance
from MooToo.names import empire_names
from MooToo.constants import StarColour
from MooToo.empire import Empire


if TYPE_CHECKING:
    from MooToo.system import System


NUM_SYSTEMS = 40
NUM_EMPIRES = 4
MAX_X = 530
MAX_Y = 420

SYSTEMS: dict[int, "System"] = {}
EMPIRES: dict[str, "Empire"] = {}
TURN_NUMBER = 0


#####################################################################################################
def populate():
    """Fill the galaxy with things"""
    positions = get_system_positions(NUM_SYSTEMS)
    for _id, _ in enumerate(range(NUM_SYSTEMS)):
        position = random.choice(positions)
        positions.remove(position)
        SYSTEMS[_id] = System(_id, position)
    for home_system in find_home_systems(NUM_EMPIRES):
        empire_name = random.choice(empire_names)
        empire_names.remove(empire_name)
        make_empire(empire_name, home_system)
    for system in SYSTEMS.values():
        system.make_orbits()


#####################################################################################################
def find_home_systems(num_empires: int) -> list["System"]:
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
        for system in SYSTEMS.values():
            distance = get_distance_tuple(position, system.position)
            if distance < min_dist:
                min_dist = distance
                min_system = system
        home_systems.append(min_system)
    return home_systems


#####################################################################################################
def turn():
    """End of turn"""
    global TURN_NUMBER
    TURN_NUMBER += 1
    for empire in EMPIRES.values():
        empire.turn()


#####################################################################################################
def make_empire(empire_name: str, home_system: "System"):
    """ """
    home_system.colour = StarColour.YELLOW
    empire = Empire(empire_name)
    EMPIRES[empire_name] = empire
    home_planet = make_home_planet(home_system)
    empire.set_home_planet(home_planet)
    home_system.orbits.append(home_planet)
    random.shuffle(home_system.orbits)


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
def save(filename: str) -> None:
    fname = f"{filename}_{TURN_NUMBER % 10}.json"
    print(f"Saving as {fname}")
    galaxy = {"turn_number": TURN_NUMBER, "systems": SYSTEMS, "empires": EMPIRES}
    with open(fname, "w") as outfh:
        outfh.write(jsonpickle.encode(galaxy, indent=2))


#####################################################################################################
def load(filename: str):
    global TURN_NUMBER, SYSTEMS, EMPIRES
    with open(filename) as infh:
        galaxy = jsonpickle.loads(infh.read())
    TURN_NUMBER = galaxy["turn_number"]
    SYSTEMS = galaxy["systems"]
    EMPIRES = galaxy["empires"]


# EOF
