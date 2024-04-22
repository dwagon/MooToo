""" system class"""

import random
from MooToo.planet import Planet
from MooToo.config import Config
from MooToo.names import system_names

MAX_ORBITS = 6
ORBIT_NAMES = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")


class System:
    def __init__(self, position: tuple[int, int], config: Config):
        self.position = position
        self.config = config
        self.name = pick_name()
        self.colour = self.pick_star_colour()
        self.draw_colour = self.config["galaxy"]["star_colours"][self.colour]["draw_colour"]
        self.planets: list[Planet] = []

    def pick_star_colour(self) -> str:
        while True:
            pct = random.randint(0, 100)
            prev = 0
            for colour, details in self.config["galaxy"]["star_colours"].items():
                if pct <= prev + details["probability"]:
                    return colour
                else:
                    prev += details["probability"]

    def make_orbits(self):
        for orbit in range(MAX_ORBITS):
            pct = random.randint(0, 100)
            if pct <= self.config["galaxy"]["star_colours"][self.colour]["prob_orbit"]:
                name = f"{self.name} {ORBIT_NAMES[orbit]}"
                self.planets[orbit] = Planet(name, self.colour)

        pass


def pick_name():
    """Pick a system name"""
    name = random.choice(system_names)
    system_names.remove(name)
    return name


# EOF
