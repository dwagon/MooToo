""" Relating to player's empires"""

from collections import defaultdict
from typing import TYPE_CHECKING

from MooToo.constants import PlanetClimate, PlanetSize, Building, Technology
from MooToo.system import System
from MooToo.planet import Planet, PopulationJobs
from MooToo.research import ResearchCategory
from MooToo.ship import Ship

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, name: str, galaxy: "Galaxy"):
        self.name = name
        self.galaxy = galaxy
        self.government = "Feudal"  # Fix me
        self.home_planet = None
        self.money: int = 100
        self.income: int = 0
        self.known_systems: set[int] = set()
        self.owned_planets: list[Planet] = []
        self.ships: list[Ship] = []
        self.researching: Technology | None = None
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
        self.known_techs: set[Technology] = {
            Technology.STAR_BASE,
            Technology.MARINE_BARRACKS,
            Technology.COLONY_BASE,
        }

    #####################################################################################################
    def add_ship(self, ship: Ship, system: System):
        self.ships.append(ship)
        ship.orbit = system
        ship.location = system.position

    #####################################################################################################
    def turn(self):
        """Have a turn"""
        self.research_spent += self.get_research_points()
        if self.researching and self.research_spent > self.galaxy.get_research(self.researching).cost:
            self.learnt(self.researching)
            self.researching = None
        income = 0
        for planet in self.owned_planets:
            planet.turn()
            income += planet.money_production() - planet.money_cost()
        for ship in self.ships:
            ship.turn()
            if ship.orbit:
                self.know_system(ship.orbit)
        self.income = income
        self.money += self.income

    #####################################################################################################
    def start_researching(self, to_research: Technology) -> None:
        self.researching = to_research

    #####################################################################################################
    def learnt(self, tech: Technology) -> None:
        """We have researched {research}"""
        self.known_techs.add(tech)
        research = self.galaxy.get_research(tech)
        self.researched[research.category] = research.cost

    #####################################################################################################
    def next_research(self, category: ResearchCategory) -> list[Technology]:
        """What are the next techs that can be researched"""
        available: dict[int, list[Technology]] = defaultdict(list)

        for tech, research in self.galaxy._researches.items():
            if research.category != category:
                continue
            if tech in self.known_techs:
                continue
            if research.cost <= self.researched[category]:
                continue

            available[research.cost].append(tech)
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
        """Return a suitable home planet in {system}"""
        p = Planet(f"{self.name} Home", system, self.galaxy)
        p.make_home_world()
        p.owner = self.name
        self.owned_planets.append(p)
        p.population = 8e6
        p.climate = PlanetClimate.TERRAN
        p.size = PlanetSize.LARGE
        p.jobs[PopulationJobs.FARMER] = 4
        p.jobs[PopulationJobs.WORKERS] = 2
        p.jobs[PopulationJobs.SCIENTISTS] = 2
        p.build_queue = []
        p.buildings.add(Building.MARINE_BARRACKS)
        p.buildings.add(Building.STAR_BASE)
        self.know_system(system)

        p.gen_climate_image()
        return p
