""" Planet class """

import math
import random
from typing import TYPE_CHECKING, Optional

from MooToo.utils import prob_map, get_research, get_building
from MooToo.constants import PlanetGravity, PlanetSize, PlanetCategory, PlanetRichness, PlanetClimate, Technology
from MooToo.constants import PopulationJobs, STAR_COLOURS, POP_SIZE_MAP, POP_CLIMATE_MAP, FOOD_CLIMATE_MAP
from MooToo.planet_building import Building
from MooToo.planet_work import work_surplus
from MooToo.build_queue import BuildQueue
from MooToo.construct import Construct, ConstructType
from MooToo.ship import ShipType

if TYPE_CHECKING:
    from MooToo.system import System
    from MooToo.empire import Empire


#####################################################################################################
#####################################################################################################
#####################################################################################################
class Planet:
    def __init__(self, system: "System", **kwargs):
        self.name = ""
        self.system = system

        self._owner: str = ""
        self.jobs = {PopulationJobs.FARMERS: 0, PopulationJobs.WORKERS: 0, PopulationJobs.SCIENTISTS: 0}
        self.category = kwargs.get("category", pick_planet_category())
        self.size = kwargs.get("size", pick_planet_size())
        self.richness = kwargs.get("richness", pick_planet_richness(STAR_COLOURS[self.system.colour]["richness"]))
        self.climate = kwargs.get("climate", pick_planet_climate(STAR_COLOURS[self.system.colour]["climate"]))
        self.gravity = kwargs.get("gravity", pick_planet_gravity(self.size, self.richness))
        self._population = 0.0
        self.buildings: set[Building] = set()  # Built buildings
        self._buildings_available: set[Building] = set()
        self.build_queue = BuildQueue(self)
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
        if not self.build_queue or not work_surplus(self):
            return 0
        if self.build_queue.is_building(Building.TRADE_GOODS) or self.build_queue.is_building(Building.HOUSING):
            return 0
        return min(10000, (self.build_queue.cost - self.construction_spent) // work_surplus(self))

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
    def remove_workers(self, num: int, job: PopulationJobs) -> int:
        """Remove workers from a job"""
        num = min(self.jobs[job], num)
        self.jobs[job] -= num
        return num

    #####################################################################################################
    def add_workers(self, num: int, job: PopulationJobs):
        """Add workers to a job"""
        self.jobs[job] += num

    #####################################################################################################
    def move_workers(self, num: int, src_job: PopulationJobs, target_job: PopulationJobs):
        """Move workers from a job to another"""
        num = self.remove_workers(num, src_job)
        self.add_workers(num, target_job)

    #####################################################################################################
    def colonize(self, owner: str) -> None:
        """Make the planet an active colony"""
        if FOOD_CLIMATE_MAP[self.climate]:
            self.jobs[PopulationJobs.FARMERS] = 1
        else:
            self.jobs[PopulationJobs.WORKERS] = 1
        self._population = 1e6
        self.owner = owner
        self.owner.own_planet(self)

    #####################################################################################################
    def building_production(self) -> None:
        """Produce buildings"""
        if not self.build_queue:
            return
        self.construction_spent += work_surplus(self)
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
                if not construct.ship.built():
                    self.owner.delete_ship(construct.ship)

    #####################################################################################################
    def grow_population(self) -> None:
        from MooToo.food import food_surplus

        old_pop = int(self._population / 1e6)
        self._population += self.population_increment()
        if int(self._population / 1e6) > old_pop:
            for _ in range(int(self._population / 1e6) - old_pop):  # Assign to new jobs
                if FOOD_CLIMATE_MAP[self.climate] and food_surplus(self) < 5:
                    self.jobs[PopulationJobs.FARMERS] += 1
                else:
                    self.jobs[PopulationJobs.WORKERS] += 1

    #####################################################################################################
    def population_increment(self) -> int:
        """How much population will grow this turn
        See https://strategywiki.org/wiki/Master_of_Orion_II:_Battle_at_Antares/Calculations
        """
        from MooToo.food import food_surplus

        race_bonus = 0  # TBA: Racial growth bonus
        medicine_bonus = 0  # TBA: medical skill bonus
        if self.build_queue.is_building(Building.HOUSING):
            housing_bonus = int((work_surplus(self) * 40) / (self._population / 1e6))
        else:
            housing_bonus = 0
        if self.current_population() == self.max_population():
            return 0
        max_pop = self.max_population() * 1e6
        if food_surplus(self) < 0:
            food_lack_penalty = -50 * food_surplus(self)
        else:
            food_lack_penalty = 0
        free_space = max_pop - self._population
        basic_increment = int(math.sqrt(2000 * self._population * free_space / max_pop))
        population_inc = (
            int(basic_increment * (100 + race_bonus + medicine_bonus + housing_bonus) / 100) - food_lack_penalty
        )
        if Building.CLONING_CENTER in self.buildings:
            population_inc += 100_000
        return population_inc

    #####################################################################################################
    def current_population(self) -> int:
        return int(self._population / 1e6)

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
        category = self.category.name
        richness = self.richness.name
        climate = self.climate.name

        return f"<Planet {self.name}: {category} {self.size.name} {richness} {climate} {self.gravity.name}>"


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
