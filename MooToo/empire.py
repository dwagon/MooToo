""" Relating to player's empires"""

from collections import defaultdict
from typing import TYPE_CHECKING

from MooToo.system import System
from MooToo.planet import Planet, PopulationJobs
from MooToo.research import Research, ResearchCategory
from MooToo.ship import Ship

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, name: str, home_planet: System, galaxy: "Galaxy"):
        self.name = name
        self.galaxy = galaxy
        self.government = "Feudal"  # Fix me
        self.home_planet = home_planet
        self.money = 100
        self.income = 0
        self.known_systems: set[int] = set()
        self.owned_planets: list[Planet] = []
        self.ships: list[Ship] = []
        self.researching: Research | None = None
        self.research_spent = 0
        self.researched: dict[ResearchCategory, int] = {
            ResearchCategory.FORCE_FIELDS: 0,
            ResearchCategory.BIOLOGY: 0,
            ResearchCategory.POWER: 0,
            ResearchCategory.PHYSICS: 0,
            ResearchCategory.COMPUTERS: 0,
            ResearchCategory.SOCIOLOGY: 0,
            ResearchCategory.CONSTRUCTION: 0,
            ResearchCategory.CHEMISTRY: 0,
        }  # What category / price has been researched
        self.known_techs: dict[str, Research] = {
            "Star Base": galaxy.researches["Star Base"],
            "Marine Barracks": galaxy.researches["Marine Barracks"],
            "Colony Base": galaxy.researches["Colony Base"],
        }

    #####################################################################################################
    def add_ship(self, ship: Ship, system: System):
        self.ships.append(ship)
        ship.location = system

    #####################################################################################################
    def turn(self):
        """Have a turn"""
        income = 0
        for planet in self.owned_planets:
            planet.turn()
            income += planet.money_production() - planet.money_cost()
        self.income = income
        self.money += self.income
        self.research_spent += self.get_research_points()
        if self.researching and self.research_spent > self.researching.cost:
            self.known_techs[self.researching.name] = self.researching
            self.researched[self.researching.category] = self.researching.cost
            self.researching = None

    #####################################################################################################
    def next_research(self, category: ResearchCategory) -> list[Research]:
        """What are the next techs that can be researched"""
        available: dict[int, list[Research]] = defaultdict(list)

        for name, research in self.galaxy.researches.items():
            if research.category != category:
                continue
            if name in self.known_techs:
                continue
            if research.cost <= self.researched[category]:
                continue

            available[research.cost].append(research)
        if not available:
            return []
        next_batch_cost = min(list(available.keys()))

        return available[next_batch_cost]

    #####################################################################################################
    def get_research_points(self) -> int:
        rp = 0
        for planet in self.owned_planets:
            rp += planet.get_research_points()
        return rp

    #####################################################################################################
    def know_system(self, system: System) -> None:
        self.known_systems.add(system.id)

    #####################################################################################################
    def is_known_system(self, system: System) -> bool:
        """Is the system known to this empire"""
        return system.id in self.known_systems

    #####################################################################################################

    def make_home_planet(self, system: "System") -> Planet:
        """Return a suitable home planet"""
        p = Planet(f"{self.name} Home", system, self.galaxy)
        p.make_home_world()
        p.owner = self.name
        self.owned_planets.append(p)
        p.population = 8e6
        p.jobs[PopulationJobs.FARMER] = 4
        p.jobs[PopulationJobs.WORKERS] = 2
        p.jobs[PopulationJobs.SCIENTISTS] = 2
        p.build_queue = []
        p.buildings["Marine Barracks"] = self.galaxy.buildings["Marine Barracks"]
        p.buildings["Star Base"] = self.galaxy.buildings["Star Base"]

        p.gen_climate_image()
        return p
