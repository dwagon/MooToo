""" Planet class """

import math
import random
from typing import TYPE_CHECKING, Optional
from MooToo.utils import prob_map
from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import (
    PlanetCategory,
    PopulationJobs,
    PlanetRichness,
    PlanetClimate,
    PlanetGravity,
    PlanetSize,
    StarColour,
)
from MooToo.ship import ShipType, Ship, select_ship_type_by_name

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy

#####################################################################################################
STAR_COLOURS = {
    StarColour.BLUE: {
        "climate": {
            "Toxic": 16,
            "Radiated": 50,
            "Barren": 27,
            "Desert": 7,
            "Tundra": 0,
            "Ocean": 0,
            "Swamp": 0,
            "Arid": 0,
            "Terran": 0,
            "Gaia": 0,
        },
        "richness": {"Ultra Poor": 0, "Poor": 0, "Abundant": 40, "Rich": 20, "Ultra Rich": 20},
    },
    StarColour.WHITE: {
        "climate": {
            "Toxic": 16,
            "Radiated": 37,
            "Barren": 27,
            "Desert": 6,
            "Tundra": 4,
            "Ocean": 2,
            "Swamp": 1,
            "Arid": 3,
            "Terran": 3,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 0, "Poor": 20, "Abundant": 40, "Rich": 30, "Ultra Rich": 10},
    },
    StarColour.YELLOW: {
        "climate": {
            "Toxic": 12,
            "Radiated": 27,
            "Barren": 30,
            "Desert": 6,
            "Tundra": 8,
            "Ocean": 5,
            "Swamp": 4,
            "Arid": 3,
            "Terran": 4,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 0, "Poor": 30, "Abundant": 40, "Rich": 20, "Ultra Rich": 10},
    },
    StarColour.ORANGE: {
        "climate": {
            "Toxic": 16,
            "Radiated": 17,
            "Barren": 23,
            "Desert": 8,
            "Tundra": 7,
            "Ocean": 6,
            "Swamp": 7,
            "Arid": 6,
            "Terran": 7,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 10, "Poor": 40, "Abundant": 40, "Rich": 10, "Ultra Rich": 0},
    },
    StarColour.RED: {
        "climate": {
            "Toxic": 16,
            "Radiated": 13,
            "Barren": 50,
            "Desert": 3,
            "Tundra": 7,
            "Ocean": 2,
            "Swamp": 2,
            "Arid": 2,
            "Terran": 4,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 20, "Poor": 40, "Abundant": 40, "Rich": 0, "Ultra Rich": 0},
    },
    StarColour.BROWN: {
        "climate": {
            "Toxic": 20,
            "Radiated": 30,
            "Barren": 10,
            "Desert": 20,
            "Tundra": 10,
            "Ocean": 2,
            "Swamp": 2,
            "Arid": 2,
            "Terran": 3,
            "Gaia": 1,
        },
        "richness": {"Ultra Poor": 5, "Poor": 10, "Abundant": 60, "Rich": 20, "Ultra Rich": 5},
    },
}
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
    def __init__(self, name: str, system, galaxy: "Galaxy"):
        self.name = name
        self.system = system
        self._galaxy = galaxy
        self.category = pick_planet_category()
        self.size = pick_planet_size()
        self.richness = pick_planet_richness(STAR_COLOURS[self.system.colour]["richness"])
        self.climate = pick_planet_climate(STAR_COLOURS[self.system.colour]["climate"])
        self.gravity = pick_planet_gravity(self.size, self.richness)
        self._owner: str = ""
        self.jobs = {PopulationJobs.FARMER: 0, PopulationJobs.WORKERS: 0, PopulationJobs.SCIENTISTS: 0}
        self.population = 0.0
        self.buildings: dict[str, PlanetBuilding] = {}
        self.buildings_available: dict[str, PlanetBuilding] = {}
        self.build_queue: list[PlanetBuilding | Ship] = []
        self.construction_spent = 0
        self.arc = random.randint(0, 359)
        self.climate_image = self.gen_climate_image()

    #####################################################################################################
    @property
    def galaxy(self) -> "Galaxy":
        assert self._galaxy
        return self._galaxy

    @galaxy.setter
    def galaxy(self, value):
        self._galaxy = value

    #####################################################################################################
    @property
    def owner(self) -> Optional[str]:
        return self.galaxy.empires.get(self._owner)

    @owner.setter
    def owner(self, value):
        self._owner = value

    #####################################################################################################
    def available_to_build(self) -> dict[str, PlanetBuilding]:
        """What buildings are available to be built on this planet"""
        avail = {}
        for name, tech in self.owner.known_techs.items():
            if building := tech.enabled_building:
                if building.available_to_build(self):
                    avail[name] = building
        return avail

    #####################################################################################################
    def gen_climate_image(self):
        num = random.randint(0, 2)
        return f"surface_{self.climate}_{num}"

    #####################################################################################################
    def get_research_points(self) -> int:
        """How many research points does this planet generate"""
        rp = 0
        for building in self.buildings.values():
            rp += building.research_bonus(self)
        rp = max(self.jobs[PopulationJobs.SCIENTISTS], rp)

        return int(rp)

    #####################################################################################################
    def morale(self) -> int:
        """Morale of planet (out of 10)"""
        morale = 5
        for building in self.buildings.values():
            morale += building.morale_bonus(self)
        return morale

    #####################################################################################################
    def max_population(self) -> int:
        """What's the maximum population this planet can support"""
        max_pop = POP_SIZE_MAP[self.size] * POP_CLIMATE_MAP[self.climate]
        for building in self.buildings.values():
            max_pop += building.max_pop_bonus(self)
        return max_pop

    #####################################################################################################
    def turn(self):
        """New turn"""
        self.arc = random.randint(0, 359)
        if not self.owner:
            return
        self.owner.money += self.money_production()
        self.owner.money -= self.money_cost()
        self.building_production()
        self.grow_population()
        self.buildings_available = self.available_to_build()

    #####################################################################################################
    def building_production(self) -> None:
        """Produce buildings"""
        self.construction_spent += self.work_production()
        if not self.build_queue:
            return
        if self.construction_spent >= self.build_queue[0].cost:
            self.construction_spent -= self.build_queue[0].cost
            self.finish_construction(self.build_queue.pop(0))

    #####################################################################################################
    def finish_construction(self, construct: PlanetBuilding | Ship):
        """Create a new building"""
        if isinstance(construct, PlanetBuilding):
            self.buildings[construct.name] = construct
        elif isinstance(construct, Ship):
            self.owner.add_ship(construct, self.system)
        else:
            print(f"finish_construction: Unknown {construct=}")

    #####################################################################################################
    def add_to_build_queue(self, building: PlanetBuilding | Ship):
        if len(self.build_queue) < 6:
            self.build_queue.append(building)

    #####################################################################################################
    def toggle_build_queue_by_name(self, building_name: str):
        """Add a building by name to the build queue, or remove it if it already exists"""
        if building_name in self.galaxy.buildings:
            building = self.galaxy.buildings[building_name]
            for bld in self.build_queue:
                if building_name == bld.name:
                    self.build_queue.remove(building)
                    return
            self.add_to_build_queue(building)
        elif building_name.lower() in ShipType:
            self.add_to_build_queue(select_ship_type_by_name(building_name))
        else:
            print(f"toggle_build_queue_by_name({building_name=}): What you talking about?")

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
        max_pop = self.max_population() * 1e6
        food_lack_penalty = 50 * self.food_lack()
        free_space = max_pop - self.population
        basic_increment = int(math.sqrt(2000 * self.population * free_space / max_pop))
        population_inc = (
            int(basic_increment * (100 + race_bonus + medicine_bonus + housing_bonus) / 100) - food_lack_penalty
        )
        if "Cloning Center" in self.buildings:
            population_inc += 100_000
        return population_inc

    #####################################################################################################
    def food_lack(self) -> int:
        """How much food do we lack"""
        if self.food_production() > self.current_population():
            return 0
        return self.current_population() - self.food_production()

    #####################################################################################################
    def money_production(self) -> int:
        """How much money the planet produces"""
        return (
            self.jobs[PopulationJobs.FARMER] + self.jobs[PopulationJobs.WORKERS] + self.jobs[PopulationJobs.SCIENTISTS]
        )

    #####################################################################################################
    def money_cost(self) -> int:
        """How much money the planet costs"""
        return sum(_.maintenance for _ in self.buildings.values())

    #####################################################################################################
    def current_population(self) -> int:
        return int(self.population / 1e6)

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
    def pollution(self) -> int:
        return 0

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
