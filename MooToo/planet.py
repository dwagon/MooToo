""" Planet class """

import random
from typing import Any
from MooToo.utils import prob_map
from MooToo.constants import PlanetCategory, PopulationJobs, PlanetRichness, PlanetClimate, PlanetGravity, PlanetSize


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

    def make_home_world(self):
        self.category = PlanetCategory.PLANET
        self.size = PlanetSize.HUGE
        self.richness = PlanetRichness.RICH
        self.climate = PlanetClimate.TERRAN
        self.gravity = PlanetGravity.NORMAL


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
        PlanetSize.TINY: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.LOW,
            PlanetRichness.POOR: PlanetGravity.LOW,
            PlanetRichness.ABUNDANT: PlanetGravity.LOW,
            PlanetRichness.RICH: PlanetGravity.NORMAL,
            PlanetRichness.ULTRA_RICH: PlanetGravity.NORMAL,
        },
        PlanetSize.SMALL: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.LOW,
            PlanetRichness.POOR: PlanetGravity.LOW,
            PlanetRichness.ABUNDANT: PlanetGravity.NORMAL,
            PlanetRichness.RICH: PlanetGravity.NORMAL,
            PlanetRichness.ULTRA_RICH: PlanetGravity.NORMAL,
        },
        PlanetSize.MEDIUM: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.LOW,
            PlanetRichness.POOR: PlanetGravity.NORMAL,
            PlanetRichness.ABUNDANT: PlanetGravity.NORMAL,
            PlanetRichness.RICH: PlanetGravity.NORMAL,
            PlanetRichness.ULTRA_RICH: PlanetGravity.HIGH,
        },
        PlanetSize.LARGE: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.NORMAL,
            PlanetRichness.POOR: PlanetGravity.NORMAL,
            PlanetRichness.ABUNDANT: PlanetGravity.NORMAL,
            PlanetRichness.RICH: PlanetGravity.HIGH,
            PlanetRichness.ULTRA_RICH: PlanetGravity.HIGH,
        },
        PlanetSize.HUGE: {
            PlanetRichness.ULTRA_POOR: PlanetGravity.NORMAL,
            PlanetRichness.POOR: PlanetGravity.NORMAL,
            PlanetRichness.ABUNDANT: PlanetGravity.HIGH,
            PlanetRichness.RICH: PlanetGravity.HIGH,
            PlanetRichness.ULTRA_RICH: PlanetGravity.HIGH,
        },
    }
    gravity = grav_map[size][richness]
    return gravity


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
