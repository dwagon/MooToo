""" Planet class """

import math
import random
from typing import TYPE_CHECKING, Optional

from MooToo.utils import prob_map, get_research, get_building
from MooToo.constants import PlanetGravity, PlanetSize, PlanetCategory, PlanetRichness, PlanetClimate, Technology
from MooToo.constants import PopulationJobs, StarColour
from MooToo.planet_building import Building
from MooToo.build_queue import BuildQueue
from MooToo.construct import Construct, ConstructType
from MooToo.ship import ShipType

if TYPE_CHECKING:
    from MooToo.system import System
    from MooToo.empire import Empire

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
    def __init__(self, system: "System"):
        self.name = ""
        self.system = system
        self.category = pick_planet_category()
        self.size = pick_planet_size()
        self.richness = pick_planet_richness(STAR_COLOURS[self.system.colour]["richness"])
        self.climate = pick_planet_climate(STAR_COLOURS[self.system.colour]["climate"])
        self.gravity = pick_planet_gravity(self.size, self.richness)
        self._owner: str = ""
        self.jobs = {PopulationJobs.FARMER: 0, PopulationJobs.WORKERS: 0, PopulationJobs.SCIENTISTS: 0}
        self._population = 0.0
        self.buildings: set[Building] = set()  # Built buildings
        self._buildings_available: set[Building] = set()
        self.build_queue = BuildQueue()
        self.construction_spent = 0
        self.arc = random.randint(0, 359)
        self.climate_image = self.gen_climate_image()

    #####################################################################################################
    @property
    def owner(self) -> Optional["Empire"]:

        return self.system.galaxy.empires.get(self._owner)

    @owner.setter
    def owner(self, value: str):
        self._owner = value

    #####################################################################################################
    @property
    def buildings_available(self) -> set[Building]:
        if not self._buildings_available:
            self._buildings_available = self.available_to_build()
        return self._buildings_available

    #####################################################################################################
    def __getitem__(self, item):
        return get_building(item)

    #####################################################################################################
    def buy_cost(self) -> int:
        """How much to buy production"""
        pct_complete = self.construction_spent / self.build_queue.cost
        if pct_complete > 0.5:
            return int(2 * self.build_queue.cost - self.construction_spent * 2)
        if pct_complete > 0.1:
            return int(3.5 * self.build_queue.cost - self.construction_spent * 5)
        if pct_complete > 0:
            return int(4 * self.build_queue.cost - self.construction_spent * 10)
        return self.build_queue.cost * 4

    #####################################################################################################
    def turns_to_build(self) -> int:
        """How many turns left to build what we are building"""
        if not self.build_queue or not self.work_production():
            return 0
        if self.build_queue.is_building(Building.TRADE_GOODS) or self.build_queue.is_building(Building.HOUSING):
            return 0
        return min(10000, (self.build_queue.cost - self.construction_spent) // self.work_production())

    #####################################################################################################
    def can_build_big_ships(self) -> bool:
        return (
            Building.STAR_BASE in self.buildings
            or Building.BATTLESTATION in self.buildings
            or Building.STAR_FORTRESS in self.buildings
        )

    #####################################################################################################
    def available_to_build(self) -> set[Building]:
        """What buildings are available to be built on this planet"""
        avail: set[Building] = {Building.TRADE_GOODS, Building.HOUSING}
        if not self.owner:
            return set()
        for tech in self.owner.known_techs:
            if building := get_research(tech).enabled_building:
                if building.available_to_build(self):
                    avail.add(building.tag)
        return avail

    #####################################################################################################
    def gen_climate_image(self):
        num = random.randint(0, 2)
        return f"surface_{self.climate}_{num}"

    #####################################################################################################
    def research_per(self) -> int:
        per = 1
        for building in self.buildings:
            per += get_building(building).research_per_bonus(self)
        return per

    #####################################################################################################
    def get_research_points(self) -> int:
        """How many research points does this planet generate"""
        rp = 0
        for building in self.buildings:
            rp += get_building(building).research_bonus(self)
        rp += self.jobs[PopulationJobs.SCIENTISTS] * self.research_per()
        rp = max(self.jobs[PopulationJobs.SCIENTISTS], rp)

        return int(rp)

    #####################################################################################################
    def morale(self) -> int:
        """Morale of planet (out of 10)"""
        morale = 5
        for building in self.buildings:
            morale += get_building(building).morale_bonus(self)
        return morale

    #####################################################################################################
    def max_population(self) -> int:
        """What's the maximum population this planet can support"""
        max_pop = POP_SIZE_MAP[self.size] * POP_CLIMATE_MAP[self.climate]
        for building in self.buildings:
            max_pop += get_building(building).max_pop_bonus(self)
        return max_pop

    #####################################################################################################
    def turn(self):
        """New turn"""
        self.arc = random.randint(0, 359)
        if not self.owner:
            return
        self.building_production()
        self.grow_population()
        self._buildings_available = self.available_to_build()

    #####################################################################################################
    def building_production(self) -> None:
        """Produce buildings"""
        if not self.build_queue:
            return
        self.construction_spent += self.work_production()
        cost = self.build_queue.cost
        if self.build_queue.is_building(Building.HOUSING) or self.build_queue.is_building(Building.TRADE_GOODS):
            self.construction_spent = 0
        if self.construction_spent >= cost:
            self.construction_spent -= cost
            self.finish_construction(self.build_queue.pop(0))

    #####################################################################################################
    def finish_construction(self, construct: Construct) -> None:
        """Create a new building or ship"""
        match construct.category:
            case ConstructType.BUILDING:
                self.buildings.add(construct.tag)
            case ConstructType.SHIP:
                self.owner.add_ship(construct.ship, self.system)

    #####################################################################################################
    def grow_population(self) -> None:
        old_pop = int(self._population / 1e6)
        self._population += self.population_increment()
        if int(self._population / 1e6) > old_pop:
            for _ in range(int(self._population / 1e6) - old_pop):  # Assign to new jobs
                self.jobs[PopulationJobs.FARMER] += 1  # TODO: Make this cleverer

    #####################################################################################################
    def population_increment(self) -> int:
        """How much population will grow this turn
        See https://strategywiki.org/wiki/Master_of_Orion_II:_Battle_at_Antares/Calculations
        """
        race_bonus = 0  # TBA: Racial growth bonus
        medicine_bonus = 0  # TBA: medical skill bonus
        if self.build_queue.is_building(Building.HOUSING):
            housing_bonus = int((self.work_production() * 40) / (self._population / 1e6))
        else:
            housing_bonus = 0
        if self.current_population() == self.max_population():
            return 0
        max_pop = self.max_population() * 1e6
        food_lack_penalty = 50 * self.food_lack()
        free_space = max_pop - self._population
        basic_increment = int(math.sqrt(2000 * self._population * free_space / max_pop))
        population_inc = (
            int(basic_increment * (100 + race_bonus + medicine_bonus + housing_bonus) / 100) - food_lack_penalty
        )
        if Building.CLONING_CENTER in self.buildings:
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
        money = (
            self.jobs[PopulationJobs.FARMER] + self.jobs[PopulationJobs.WORKERS] + self.jobs[PopulationJobs.SCIENTISTS]
        )
        if self.build_queue.is_building(Building.TRADE_GOODS):
            money += self.work_production()
        return money

    #####################################################################################################
    def money_cost(self) -> int:
        """How much money the planet costs"""
        return sum(get_building(_).maintenance for _ in self.buildings)

    #####################################################################################################
    def current_population(self) -> int:
        return int(self._population / 1e6)

    #####################################################################################################
    def food_per(self) -> int:
        """How much food each farmer produces"""
        per = FOOD_CLIMATE_MAP[self.climate]
        for building in self.buildings:
            per += get_building(building).food_per_bonus(self)
        return per

    #####################################################################################################
    def food_production(self) -> int:
        production = self.food_per() * self.jobs[PopulationJobs.FARMER]
        production *= GRAVITY_MAP[self.gravity]
        for building in self.buildings:
            production += get_building(building).food_bonus(self)
        production = max(self.jobs[PopulationJobs.FARMER], production)
        return int(production)

    #####################################################################################################
    def food_consumption(self) -> int:
        return (
            self.jobs[PopulationJobs.FARMER] + self.jobs[PopulationJobs.WORKERS] + self.jobs[PopulationJobs.SCIENTISTS]
        )

    #####################################################################################################
    def production_per(self) -> int:
        per = PROD_RICHNESS_MAP[self.richness]
        for building in self.buildings:
            per += get_building(building).prod_per_bonus(self)
        return per

    #####################################################################################################
    def work_production(self) -> int:
        production = self.production_per() * self.jobs[PopulationJobs.WORKERS]
        production *= GRAVITY_MAP[self.gravity]
        for building in self.buildings:
            production += get_building(building).prod_bonus(self)
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
    def can_build_ship(self, ship: ShipType) -> bool:
        """Can this empire build a type of ship"""
        if not self.owner:
            return False
        # TODO - make sure there is a suitable planet in the system
        if ship == ShipType.ColonyBase:
            return True

        # Need basic tech to build anything but a colony base
        known_techs = self.owner.known_techs
        if Technology.STANDARD_FUEL_CELLS not in known_techs or Technology.NUCLEAR_DRIVE not in known_techs:
            return False

        match ship:
            case ShipType.ColonyShip:
                if Technology.COLONY_SHIP in known_techs:
                    return True
            case ShipType.OutpostShip:
                if Technology.OUTPOST_SHIP in known_techs:
                    return True
            case ShipType.Transport:
                if Technology.TRANSPORT in known_techs and Building.MARINE_BARRACKS in self.buildings:
                    return True
            case ShipType.Frigate | ShipType.Destroyer:
                return True
            case ShipType.Cruiser | ShipType.Battleship:
                if self.can_build_big_ships():
                    return True
            case ShipType.Titan:
                if Technology.TITAN_CONSTRUCTION in known_techs and self.can_build_big_ships():
                    return True
            case ShipType.DoomStar:
                if Technology.DOOM_STAR_CONSTRUCTION in known_techs and self.can_build_big_ships():
                    return True
        return False

    #####################################################################################################
    def __repr__(self):
        return f"<Planet {self.name}: {self.category.name} {self.size.name} {self.richness.name} {self.climate.name} {self.gravity.name}>"


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


#####################################################################################################
def make_home_planet(system: "System") -> Planet:
    """Return a suitable home planet in {system}"""
    p = Planet(system)
    p.climate = PlanetClimate.TERRAN
    p.size = PlanetSize.LARGE
    p.category = PlanetCategory.PLANET
    p.richness = PlanetRichness.ABUNDANT
    p.gravity = PlanetGravity.NORMAL
    p.climate_image = p.gen_climate_image()
    return p
