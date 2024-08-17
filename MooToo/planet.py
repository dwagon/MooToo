""" Planet class """

import math
import random
from typing import TYPE_CHECKING

from MooToo.utils import get_research, get_building, EmpireId, PlanetId, SystemId
from MooToo.constants import Technology
from MooToo.constants import (
    PopulationJobs,
    POP_SIZE_MAP,
    POP_CLIMATE_MAP,
    FOOD_CLIMATE_MAP,
    PlanetSize,
    PlanetRichness,
    PlanetGravity,
    PlanetCategory,
    PlanetClimate,
)
from MooToo.planet_building import Building
from MooToo.planet_work import work_surplus
from MooToo.build_queue import BuildQueue
from MooToo.construct import Construct, ConstructType
from MooToo.ship import ShipType

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
#####################################################################################################
#####################################################################################################
class Planet:
    def __init__(self, planet_id: PlanetId, system_id: SystemId, galaxy: "Galaxy", **kwargs):
        self.id = planet_id
        self.name = ""
        self.system_id = system_id
        self.galaxy = galaxy

        self.owner: EmpireId = 0
        self.jobs = {PopulationJobs.FARMERS: 0, PopulationJobs.WORKERS: 0, PopulationJobs.SCIENTISTS: 0}
        self.category = kwargs.get("category", PlanetCategory.PLANET)
        self.size = kwargs.get("size", PlanetSize.MEDIUM)
        self.richness = kwargs.get("richness", PlanetRichness.ABUNDANT)
        self.climate = kwargs.get("climate", PlanetClimate.TERRAN)
        self.gravity = kwargs.get("gravity", PlanetGravity.NORMAL)
        self.raw_population = 0.0
        self.buildings: set[Building] = set()  # Built buildings
        self.build_queue = BuildQueue(self)
        self.construction_spent = 0
        self.arc = random.randint(0, 359)
        self.climate_image = self.gen_climate_image()

    #####################################################################################################
    def __getitem__(self, item):
        return get_building(item)

    #####################################################################################################
    def buy_cost(self) -> int:
        """How much to buy production"""
        pct_complete = self.construction_spent / self.build_queue.cost
        if self.construction_spent == 0:
            return self.build_queue.cost * 4
        if pct_complete > 0.5:
            return int(2 * self.build_queue.cost - self.construction_spent * 2)
        if pct_complete > 0.1:
            return int(3.5 * self.build_queue.cost - self.construction_spent * 5)
        return int(4 * self.build_queue.cost - self.construction_spent * 10)

    #####################################################################################################
    def turns_to_build(self) -> int:
        """How many turns left to build what we are building"""
        if not self.build_queue or not work_surplus(self):
            return 0
        if self.build_queue.is_building(Building.TRADE_GOODS) or self.build_queue.is_building(Building.HOUSING):
            return 0
        return min(10000, (self.build_queue.cost - self.construction_spent) // work_surplus(self))

    #####################################################################################################
    def _can_build_big_ships(self) -> bool:
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
        for tech in self.galaxy.empires[self.owner].known_techs:
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
        self._building_production()
        self._grow_population()

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
    def colonize(self, owner: EmpireId) -> None:
        """Make the planet an active colony"""
        if FOOD_CLIMATE_MAP[self.climate]:
            self.jobs[PopulationJobs.FARMERS] = 1
        else:
            self.jobs[PopulationJobs.WORKERS] = 1
        self.raw_population = 1e6
        self.owner = owner
        self.galaxy.empires[self.owner].own_planet(self.id)

    #####################################################################################################
    def _building_production(self) -> None:
        """Produce buildings"""
        if not self.build_queue:
            return
        self.construction_spent += work_surplus(self)
        cost = self.build_queue.cost
        if self.build_queue.is_building(Building.HOUSING) or self.build_queue.is_building(Building.TRADE_GOODS):
            self.construction_spent = 0
        if self.construction_spent >= cost:
            self.construction_spent -= cost
            self._finish_construction(self.build_queue.pop(0))

    #####################################################################################################
    def _finish_construction(self, construct: Construct) -> None:
        """Create a new building or ship"""
        match construct.category:
            case ConstructType.BUILDING:
                self.buildings.add(construct.tag)
            case ConstructType.SHIP:
                self.galaxy.empires[self.owner].add_ship(construct.ship.id, self.system_id)
                if not construct.ship.built():
                    self.galaxy.empires[self.owner].delete_ship(construct.ship.id)
            case ConstructType.FREIGHTER:
                self.galaxy.empires[self.owner].freighters += 5

    #####################################################################################################
    def _grow_population(self) -> None:
        from MooToo.planet_food import food_surplus

        old_pop = int(self.raw_population / 1e6)
        self.raw_population += self.population_increment()
        if int(self.raw_population / 1e6) > old_pop:
            for _ in range(int(self.raw_population / 1e6) - old_pop):  # Assign to new jobs
                if FOOD_CLIMATE_MAP[self.climate] and food_surplus(self) < 5:
                    self.jobs[PopulationJobs.FARMERS] += 1
                else:
                    self.jobs[PopulationJobs.WORKERS] += 1

    #####################################################################################################
    def population_increment(self) -> int:
        """How much population will grow this turn
        See https://strategywiki.org/wiki/Master_of_Orion_II:_Battle_at_Antares/Calculations
        """
        from MooToo.planet_food import food_surplus

        race_bonus = 0  # TBA: Racial growth bonus
        medicine_bonus = 0  # TBA: medical skill bonus
        if self.build_queue.is_building(Building.HOUSING):
            housing_bonus = int((work_surplus(self) * 40) / (self.raw_population / 1e6))
        else:
            housing_bonus = 0
        if self.current_population() == self.max_population():
            return 0
        max_pop = self.max_population() * 1e6
        if food_surplus(self) < 0:
            food_lack_penalty = -50 * food_surplus(self)
        else:
            food_lack_penalty = 0
        free_space = max_pop - self.raw_population
        basic_increment = int(math.sqrt(2000 * self.raw_population * free_space / max_pop))
        population_inc = (
            int(basic_increment * (100 + race_bonus + medicine_bonus + housing_bonus) / 100) - food_lack_penalty
        )
        if Building.CLONING_CENTER in self.buildings:
            population_inc += 100_000
        return population_inc

    #####################################################################################################
    def current_population(self) -> int:
        return int(self.raw_population / 1e6)

    #####################################################################################################
    def can_build(self, con: ConstructType) -> bool:
        if not self.owner:
            return False
        match con:
            case ConstructType.SPY:
                return True
            case ConstructType.FREIGHTER:
                return Technology.FREIGHTERS in self.galaxy.empires[self.owner].known_techs
            case ConstructType.COLONY_BASE:
                system = self.galaxy.systems[self.system_id]
                return system.unoccupied_planet()
        return False

    #####################################################################################################
    def can_build_ship(self, ship_type: ShipType) -> bool:
        """Can this empire build a type of ship"""
        if not self.owner:
            return False

        # Need basic tech to build anything but a colony base
        known_techs = self.galaxy.empires[self.owner].known_techs
        if Technology.STANDARD_FUEL_CELLS not in known_techs or Technology.NUCLEAR_DRIVE not in known_techs:
            return False

        match ship_type:
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
                if self._can_build_big_ships():
                    return True
            case ShipType.Titan:
                if Technology.TITAN_CONSTRUCTION in known_techs and self._can_build_big_ships():
                    return True
            case ShipType.DoomStar:
                if Technology.DOOM_STAR_CONSTRUCTION in known_techs and self._can_build_big_ships():
                    return True
        return False

    #####################################################################################################
    def __repr__(self):
        category = self.category.name
        richness = self.richness.name
        climate = self.climate.name

        return f"<Planet {self.id} {self.name}: {category} {self.size.name} {richness} {climate} {self.gravity.name}>"
