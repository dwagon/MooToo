""" Relating to player's empires"""

from collections import defaultdict
from typing import TYPE_CHECKING
from MooToo import Technology, PopulationJobs
from MooToo.research import TechCategory
from MooToo.planet_building import Building

if TYPE_CHECKING:
    from MooToo import System, Planet, Ship, Galaxy


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, name: str, galaxy: "Galaxy"):
        self.name = name
        self.galaxy = galaxy
        self.government = "Feudal"  # Fix me
        self.money: int = 100
        self.income: int = 0
        self.known_systems: set[int] = set()
        self.owned_planets: list[Planet] = []
        self.ships: list[Ship] = []
        self.researching: Technology | None = None
        self.research_spent = 0
        self.researched: dict[TechCategory, int] = {
            TechCategory.FORCE_FIELDS: 0,
            TechCategory.BIOLOGY: 0,
            TechCategory.POWER: 0,
            TechCategory.PHYSICS: 0,
            TechCategory.COMPUTERS: 0,
            TechCategory.SOCIOLOGY: 0,
            TechCategory.CONSTRUCTION: 0,
            TechCategory.CHEMISTRY: 0,
        }  # What category / price has been researched
        self.known_techs: set[Technology] = {
            Technology.STAR_BASE,
            Technology.MARINE_BARRACKS,
            Technology.COLONY_BASE,
        }

    #####################################################################################################
    def set_home_planet(self, planet: "Planet"):
        """Make planet the home planet of the empire"""
        planet.name = f"{self.name} Home"
        planet.owner = self.name
        planet._population = 8e6
        planet.jobs[PopulationJobs.FARMER] = 4
        planet.jobs[PopulationJobs.WORKERS] = 2
        planet.jobs[PopulationJobs.SCIENTISTS] = 2
        planet._buildings.add(Building.MARINE_BARRACKS)
        planet._buildings.add(Building.STAR_BASE)
        self.owned_planets.append(planet)
        self.know_system(planet.system)

    #####################################################################################################
    def add_ship(self, ship: "Ship", system: "System"):
        self.ships.append(ship)
        ship.orbit = system
        ship.location = system.position

    #####################################################################################################
    def turn(self):
        """Have a turn"""
        self.research_spent += self.get_research_points()
        if self.researching and self.research_spent > self.galaxy.get_research(self.researching).cost:
            self.research_spent -= self.galaxy.get_research(self.researching).cost
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
        print(f"DBG Starting to research {to_research}")
        self.researching = to_research

    #####################################################################################################
    def learnt(self, tech: Technology) -> None:
        """We have researched {tech}"""
        self.known_techs.add(tech)
        research = self.galaxy.get_research(tech)
        if research.general:
            for tech in research.general:
                self.known_techs.add(tech)
        self.researched[research.category] = research.cost

    #####################################################################################################
    def next_research(self, category: "TechCategory") -> list[Technology]:
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
    def know_system(self, system: "System") -> None:
        self.known_systems.add(system.id)

    #####################################################################################################
    def is_known_system(self, system: "System") -> bool:
        """Is the system known to this empire"""
        return system.id in self.known_systems
