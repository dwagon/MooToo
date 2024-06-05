""" system class"""

import random
from typing import TYPE_CHECKING
from MooToo.planet import Planet
from MooToo.names import system_names
from MooToo.constants import StarColour
from MooToo.ship import Ship

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy

#####################################################################################################

MAX_ORBITS = 5
ORBIT_NAMES = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")


STAR_COLOURS = {
    StarColour.BLUE: {
        "probability": 2,
        "prob_orbit": 40,
    },
    StarColour.WHITE: {
        "probability": 3,
        "prob_orbit": 35,
    },
    StarColour.YELLOW: {
        "probability": 10,
        "prob_orbit": 45,
    },
    StarColour.ORANGE: {
        "probability": 12,
        "prob_orbit": 45,
    },
    StarColour.RED: {
        "probability": 68,
        "prob_orbit": 35,
    },
    StarColour.BROWN: {
        "probability": 5,
        "prob_orbit": 25,
    },
}


#####################################################################################################
class System:
    def __init__(self, id, position: tuple[int, int], galaxy: "Galaxy"):
        self.id = id
        self.position = position
        self.galaxy = galaxy
        self.name = pick_name()
        self.colour = self.pick_star_colour()
        self.orbits: list[Planet | None] = []

    #####################################################################################################
    def __repr__(self):
        return f"<System {self.position}>"

    #####################################################################################################
    def pick_star_colour(self) -> str:
        while True:
            pct = random.randint(0, 100)
            prev = 0
            for colour, details in STAR_COLOURS.items():
                if pct <= prev + details["probability"]:
                    return StarColour(colour)
                else:
                    prev += details["probability"]

    #####################################################################################################
    def ships_in_orbit(self) -> list[Ship]:
        """Return the list of ships (of all players) in orbit"""
        ships: list[Ship] = []
        for emp in self.galaxy.empires.values():
            ships.extend([_ for _ in emp.ships if _.location == self])
        return ships

    #####################################################################################################
    def make_orbits(self):
        for _ in range(MAX_ORBITS):
            pct = random.randint(0, 100)
            if pct <= STAR_COLOURS[self.colour]["prob_orbit"]:
                self.orbits.append(Planet("", self, self.galaxy))
            else:
                self.orbits.append(None)

        # Name the planets
        random.shuffle(self.orbits)
        name_index = 0
        for orbit in self.orbits:
            if orbit:
                if not orbit.name:
                    orbit.name = f"{self.name} {ORBIT_NAMES[name_index]}"
                name_index += 1


#####################################################################################################
def pick_name():
    """Pick a system name"""
    name = random.choice(system_names)
    system_names.remove(name)
    return name


# EOF
