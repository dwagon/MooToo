""" Planet class """

import random
from typing import Any
from enum import Enum, StrEnum, auto
from MooToo.utils import prob_map


class PlanetCategory(Enum):
    ASTEROID = auto()
    PLANET = auto()
    GAS_GIANT = auto()


class PlanetSize(StrEnum):
    TINY = "T"
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    HUGE = "H"


class PlanetGravity(StrEnum):
    LOW = "L"
    NORMAL = "N"
    HIGH = "H"


class PlanetRichness(Enum):
    ULTRA_POOR = "UP"
    POOR = "P"
    ABUNDANT = "A"
    RICH = "R"
    ULTRA_RICH = "UR"


class PlanetClimate(StrEnum):
    TOXIC = "TX"
    RADIATED = "R"
    BARREN = "B"
    DESERT = "D"
    TUNDRA = "TU"
    OCEAN = "O"
    SWAMP = "S"
    ARID = "A"
    TERRAN = "TE"
    GAIA = "G"


class PopulationJobs(StrEnum):
    FARMER = "F"
    WORKERS = "W"
    SCIENTISTS = "S"


class Planet:
    def __init__(self, name: str, orbit: int, config: dict[str, Any]):
        self.name = name
        self.orbit = orbit
        self.category = pick_planet_category()
        self.size = pick_planet_size()
        self.richness = pick_planet_richness(config["richness"])
        self.climate = pick_planet_climate(config["climate"])
        self.gravity = pick_planet_gravity(self.size, self.richness)
        self.owner = None
        self.population = {PopulationJobs.FARMER: 0, PopulationJobs.WORKERS: 0, PopulationJobs.SCIENTISTS: 0}
        self.buildings = {}
        self.under_construction = None

        self.arc = random.randint(0, 359)

    def __repr__(self):
        return f"<Planet {self.name}: {self.category.name} {self.size.name} {self.richness.name} {self.climate.name} {self.gravity.name}>"


def pick_planet_climate(config: dict[str, int]) -> PlanetClimate:
    """Climate of the planet depends on the star colour"""
    climate = prob_map(config)
    return PlanetClimate(climate)


def pick_planet_richness(config: dict[str, int]) -> PlanetRichness:
    richness = prob_map(config)
    return PlanetRichness(richness)


def pick_planet_gravity(size: PlanetSize, richness: PlanetRichness) -> PlanetGravity:
    """The bigger and richer the planet the higher the gravity"""
    grav_map = {
        "T": {"UP": "L", "P": "L", "A": "L", "R": "N", "UR": "N"},
        "S": {"UP": "L", "P": "L", "A": "N", "R": "N", "UR": "N"},
        "M": {"UP": "L", "P": "N", "A": "N", "R": "N", "UR": "H"},
        "L": {"UP": "N", "P": "N", "A": "N", "R": "H", "UR": "H"},
        "H": {"UP": "N", "P": "N", "A": "H", "R": "H", "UR": "H"},
    }
    gravity = grav_map[size.value][richness.value]
    return PlanetGravity(gravity)


def pick_planet_size() -> PlanetSize:
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


def pick_planet_category() -> PlanetCategory:
    """What sort of planet is this?"""
    pct = random.randrange(1, 100)
    if pct < 20:
        return PlanetCategory.ASTEROID
    if pct < 40:
        return PlanetCategory.GAS_GIANT
    return PlanetCategory.PLANET
