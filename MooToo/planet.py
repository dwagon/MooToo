""" Planet class """

import math
import random
from typing import Any
from MooToo.utils import prob_map
from MooToo.building import Building
from MooToo.constants import PlanetCategory, PopulationJobs, PlanetRichness, PlanetClimate, PlanetGravity, PlanetSize

#####################################################################################################
GRAVITY_MAP: dict[PlanetGravity, float] = {
    PlanetGravity.LOW: 0.75,
    PlanetGravity.NORMAL: 1.0,
    PlanetGravity.HIGH: 0.5,
}

POP_SIZE_MAP: dict[PlanetSize, int] = {
    PlanetSize.TINY: 1,
    PlanetSize.SMALL: 2,
    PlanetSize.MEDIUM: 4,
    PlanetSize.LARGE: 5,
    PlanetSize.HUGE: 6,
}
POP_CLIMATE_MAP: dict[PlanetClimate, int] = {
    PlanetClimate.RADIATED: 1,
    PlanetClimate.TOXIC: 1,
    PlanetClimate.BARREN: 2,
    PlanetClimate.DESERT: 2,
    PlanetClimate.TUNDRA: 2,
    PlanetClimate.OCEAN: 3,
    PlanetClimate.SWAMP: 3,
    PlanetClimate.ARID: 3,
    PlanetClimate.TERRAN: 4,
    PlanetClimate.GAIA: 5,
}

FOOD_CLIMATE_MAP: dict[PlanetClimate:int] = {
    PlanetClimate.RADIATED: 0,
    PlanetClimate.TOXIC: 0,
    PlanetClimate.BARREN: 0,
    PlanetClimate.DESERT: 1,
    PlanetClimate.TUNDRA: 1,
    PlanetClimate.OCEAN: 2,
    PlanetClimate.SWAMP: 2,
    PlanetClimate.ARID: 1,
    PlanetClimate.TERRAN: 2,
    PlanetClimate.GAIA: 3,
}

PROD_RICHNESS_MAP: dict[PlanetRichness:int] = {
    PlanetRichness.ULTRA_POOR: 1,
    PlanetRichness.POOR: 2,
    PlanetRichness.ABUNDANT: 3,
    PlanetRichness.RICH: 5,
    PlanetRichness.ULTRA_RICH: 8,
}


#####################################################################################################
#####################################################################################################
#####################################################################################################
class Planet:
    def __init__(self, name: str, orbit: int, config: dict[str, Any]):
        self.name = name
        self.orbit = orbit
        self.category = pick_planet_category()
        self.size = pick_planet_size()
        self.richness = pick_planet_richness(config["richness"])
        self.climate = pick_planet_climate(config["climate"])
        self.gravity = pick_planet_gravity(self.size, self.richness)
        num = random.randint(0, 2)
        self.climate_image = f"surface_{self.climate}_{num}"
        self.owner = None
        self.jobs = {PopulationJobs.FARMER: 0, PopulationJobs.WORKERS: 0, PopulationJobs.SCIENTISTS: 0}
        self.population = 0.0
        self.buildings = {}
        self.under_construction = None
        self.construction_cost = 0
        self.arc = random.randint(0, 359)

    #####################################################################################################
    def max_population(self) -> float:
        """What's the maximum population this planet can support"""

        return POP_SIZE_MAP[self.size] * POP_CLIMATE_MAP[self.climate] * 1e6

    #####################################################################################################
    def turn(self):
        """New turn"""
        self.arc = random.randint(0, 359)
        if not self.owner:
            return
        self.owner.money += self.money_production()
        if self.under_construction:
            self.keep_making_building()
        self.grow_population()

    #####################################################################################################
    def grow_population(self) -> None:
        old_pop = int(self.population / 1e6)
        self.population += self.population_increment()
        if int(self.population / 1e6) > old_pop:
            for _ in range(int(self.population / 1e6) - old_pop):  # Assign to new jobs
                self.jobs[PopulationJobs.FARMER] += 1  # TODO: Make this cleverer

    #####################################################################################################
    def population_increment(self) -> int:
        """How much population will grow this turn
        See https://strategywiki.org/wiki/Master_of_Orion_II:_Battle_at_Antares/Calculations
        """
        race_bonus = 0  # TBA: Racial growth bonus
        medicine_bonus = 0  # TBA: medical skill bonus
        housing_bonus = 0  # TBA: building housing
        food_lack_penalty = 50 * self.food_lack()
        free_space = self.max_population() - self.population
        basic_increment = int(math.sqrt(2000 * self.population * free_space / self.max_population()))
        population_inc = (
            int(basic_increment * (100 + race_bonus + medicine_bonus + housing_bonus) / 100) - food_lack_penalty
        )
        if "Cloning Center" in self.buildings:
            population_inc += 100
        return population_inc

    #####################################################################################################
    def food_lack(self) -> int:
        """How much food do we lack"""
        if self.food_production() > int(self.current_population() / 1e6):
            return 0
        return int(self.current_population() / 1e6) - self.food_production()

    #####################################################################################################
    def money_production(self) -> int:
        prod = (
            self.jobs[PopulationJobs.FARMER] + self.jobs[PopulationJobs.WORKERS] + self.jobs[PopulationJobs.SCIENTISTS]
        )
        maintenance = sum(_.maintenance for _ in self.buildings.values())
        return prod - maintenance

    #####################################################################################################
    def start_make_building(self, building: Building):
        self.under_construction = building
        self.construction_cost = 0

    #####################################################################################################
    def keep_making_building(self):
        prod = self.work_production()
        self.construction_cost += prod
        if self.construction_cost >= self.under_construction.cost:
            self.build_building()

    #####################################################################################################
    def build_building(self):
        """the building under construction has finished"""
        self.buildings[self.under_construction.name] = self.under_construction
        self.under_construction = None

    #####################################################################################################
    def current_population(self) -> int:
        return int(self.population)

    #####################################################################################################
    def food_production(self) -> int:
        production = FOOD_CLIMATE_MAP[self.climate] * self.jobs[PopulationJobs.FARMER]
        production *= GRAVITY_MAP[self.gravity]
        for building in self.buildings.values():
            production += building.food_bonus(self)
        production = max(self.jobs[PopulationJobs.FARMER], production)
        return int(production)

    #####################################################################################################
    def food_consumption(self) -> int:
        return (
            self.jobs[PopulationJobs.FARMER] + self.jobs[PopulationJobs.WORKERS] + self.jobs[PopulationJobs.SCIENTISTS]
        )

    #####################################################################################################
    def work_production(self) -> int:
        production = PROD_RICHNESS_MAP[self.richness] * self.jobs[PopulationJobs.WORKERS]
        production *= GRAVITY_MAP[self.gravity]
        for building in self.buildings.values():
            production += building.prod_bonus(self)
        production = max(self.jobs[PopulationJobs.WORKERS], production)

        return int(production)

    #####################################################################################################
    def science_production(self) -> int:
        production = self.jobs[PopulationJobs.SCIENTISTS]
        production *= GRAVITY_MAP[self.gravity]
        production = max(self.jobs[PopulationJobs.SCIENTISTS], production)
        return int(production)

    #####################################################################################################
    def __repr__(self):
        return f"<Planet {self.name}: {self.category.name} {self.size.name} {self.richness.name} {self.climate.name} {self.gravity.name}>"

    #####################################################################################################
    def make_home_world(self):
        self.category = PlanetCategory.PLANET
        self.size = PlanetSize.MEDIUM
        self.richness = PlanetRichness.ABUNDANT
        self.climate = PlanetClimate.TERRAN
        self.gravity = PlanetGravity.NORMAL


#####################################################################################################
def pick_planet_climate(config: dict[str, int]) -> PlanetClimate:
    """Climate of the planet depends on the star colour"""
    climate = prob_map(config)
    return PlanetClimate(climate)


#####################################################################################################
def pick_planet_richness(config: dict[str, int]) -> PlanetRichness:
    richness = prob_map(config)
    return PlanetRichness(richness)


#####################################################################################################
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
    return grav_map[size][richness]


#####################################################################################################
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


#####################################################################################################
def pick_planet_category() -> PlanetCategory:
    """What sort of planet is this?"""
    pct = random.randrange(1, 100)
    if pct < 20:
        return PlanetCategory.ASTEROID
    if pct < 40:
        return PlanetCategory.GAS_GIANT
    return PlanetCategory.PLANET
