""" Planet class """

import random
from enum import Enum, auto


class PlanetCategory(Enum):
    ASTEROID = auto()
    PLANET = auto()
    GAS_GIANT = auto()


class PlanetSize(Enum):
    TINY = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    HUGE = auto()


class Planet:
    def __init__(self, name, star_colour):
        self.name = name
        self.category = pick_planet_category()
        self.size = pick_planet_size()
        self.arc = random.randint(0, 359)


def pick_planet_size():
    pct = random.randrange(1, 100)
    if pct < 10:
        return PlanetSize.TINY
    if pct < 30:
        return PlanetSize.SMALL
    if pct < 70:
        return PlanetSize.MEDIUM
    if pct < 90:
        return PlanetSize.LARGE
    return PlanetSize.HUGE


def pick_planet_category():
    """What sort of planet is this?"""
    pct = random.randrange(1, 100)
    if pct < 20:
        return PlanetCategory.ASTEROID
    if pct < 40:
        return PlanetCategory.GAS_GIANT
    return PlanetCategory.PLANET
