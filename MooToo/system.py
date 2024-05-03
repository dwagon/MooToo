""" system class"""

import random
from enum import StrEnum
from MooToo.planet import Planet
from MooToo.config import Config
from MooToo.names import system_names

MAX_ORBITS = 5
ORBIT_NAMES = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")


#####################################################################################################
class StarColour(StrEnum):
    BLUE = "blue"
    WHITE = "white"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    BROWN = "brown"


#####################################################################################################
class System:
    def __init__(self, position: tuple[int, int], config: Config):
        self.position = position
        self.config = config
        self.name = pick_name()
        self.colour = self.pick_star_colour()
        self.draw_colour = self.config["galaxy"]["star_colours"][self.colour]["draw_colour"]
        self.orbits: dict[int, Planet | None] = {}

    #####################################################################################################
    def pick_star_colour(self) -> str:
        while True:
            pct = random.randint(0, 100)
            prev = 0
            for colour, details in self.config["galaxy"]["star_colours"].items():
                if pct <= prev + details["probability"]:
                    return StarColour(colour)
                else:
                    prev += details["probability"]

    #####################################################################################################
    def turn(self):
        """Turn"""
        for planet in self.orbits.values():
            if planet:
                planet.turn()

    #####################################################################################################
    def make_orbits(self):
        name_index = 0
        for orbit in range(MAX_ORBITS):
            if orbit in self.orbits:  # Handle existing planets such as home planets
                name_index += 1
                continue
            pct = random.randint(0, 100)
            if pct <= self.config["galaxy"]["star_colours"][self.colour]["prob_orbit"]:
                name = f"{self.name} {ORBIT_NAMES[name_index]}"
                name_index += 1
                self.orbits[orbit] = Planet(name, orbit, self.config["galaxy"]["star_colours"][self.colour])
            else:
                self.orbits[orbit] = None


#####################################################################################################
def pick_name():
    """Pick a system name"""
    name = random.choice(system_names)
    system_names.remove(name)
    return name


# EOF
