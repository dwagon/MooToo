""" Relating to player's empires"""

import random
from collections import defaultdict
from typing import TYPE_CHECKING
from MooToo.constants import Technology, PopulationJobs, StarColour
from MooToo.research import TechCategory
from MooToo.planet_building import Building
from MooToo.utils import all_research, get_research
from MooToo.planet import make_home_planet
from MooToo.planet_science import science_surplus
from MooToo.planet_money import money_surplus
from MooToo.food import food_surplus


if TYPE_CHECKING:
    from MooToo.system import System
    from MooToo.planet import Planet
    from MooToo.ship import Ship


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, name: str, colour: str):
        self.name = name
        self.colour = colour
        self.government = "Feudal"  # Fix me
        self.money: int = 100
        self.income: int = 0
        self.known_systems: set[int] = set()
        self.owned_planets: set[Planet] = set()
        self.ships: list[Ship] = []
        self.researching: Technology | None = None
        self.research_spent = 0
        self.freighters = 0
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
        self.known_techs: set[Technology] = set()
        self.migrations = []

    #####################################################################################################
    def __repr__(self):
        return f"<Empire {self.name}>"

    #####################################################################################################
    def freighters_used(self) -> int:
        need_food = 0
        have_food = 0
        for planet in self.owned_planets:
            surplus = food_surplus(planet)
            if surplus < 0:
                need_food += surplus
            elif surplus > 0:
                have_food += surplus
        freighters_needed = len(self.migrations) * 5
        freighters_needed -= min(have_food, need_food)

        return min(freighters_needed, self.freighters)

    #####################################################################################################
    def set_home_planet(self, planet: "Planet"):
        """Make planet the home planet of the empire"""
        planet.name = f"{self.name} Home"
        planet.owner = self.name
        planet._population = 8e6
        planet.jobs[PopulationJobs.FARMERS] = 4
        planet.jobs[PopulationJobs.WORKERS] = 2
        planet.jobs[PopulationJobs.SCIENTISTS] = 2
        planet.buildings.add(Building.MARINE_BARRACKS)
        planet.buildings.add(Building.STAR_BASE)
        self.owned_planets.add(planet)
        self.know_system(planet.system)

    #####################################################################################################
    def own_planet(self, planet: "Planet"):
        self.owned_planets.add(planet)

    #####################################################################################################
    def add_ship(self, ship: "Ship", system: "System"):
        self.ships.append(ship)
        ship.orbit = system
        ship.location = system.position
        ship.owner = self

    #####################################################################################################
    def delete_ship(self, ship: "Ship"):
        print(f"DBG delete_ship({ship=}")
        self.ships.remove(ship)

    #####################################################################################################
    def turn(self):
        """Have a turn"""
        self.research_spent += self.get_research_points()
        if self.researching and self.research_spent > get_research(self.researching).cost:
            self.research_spent -= get_research(self.researching).cost
            self.learnt(self.researching)
            self.researching = None
        income = 0
        for planet in self.owned_planets.copy():
            planet.turn()
            income += money_surplus(planet)
        for ship in self.ships:
            ship.turn()
            if ship.orbit:
                self.know_system(ship.orbit)
        income -= self.freighters_used() // 2
        self.income = income
        self.money += self.income

    #####################################################################################################
    def send_colony(self, dest_planet: "Planet") -> None:
        """Send a colony ship to the planet"""
        for ship in self.ships:
            if not ship.coloniser:
                continue
            if not ship.destination:
                ship.set_destination_planet(dest_planet)
                return
        # Make smarter - pick closest coloniser to dest_planet

    #####################################################################################################
    def start_researching(self, to_research: Technology) -> None:
        self.researching = to_research

    #####################################################################################################
    def learnt(self, tech: Technology) -> None:
        """We have researched {tech}"""
        self.known_techs.add(tech)
        research = get_research(tech)
        if research.general:
            for gen_tech in research.general:
                self.known_techs.add(gen_tech)
        self.researched[research.category] = research.cost

    #####################################################################################################
    def next_research(self, category: "TechCategory") -> list[Technology]:
        """What are the next techs that can be researched"""
        available: dict[int, list[Technology]] = defaultdict(list)

        for tech, research in all_research().items():
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
            rp += science_surplus(planet)
        return rp

    #####################################################################################################
    def has_interest_in(self, system: "System") -> bool:
        for planet in system.orbits:
            if planet and planet.owner == self:
                return True
        return False

    #####################################################################################################
    def know_system(self, system: "System") -> None:
        self.known_systems.add(system.id)

    #####################################################################################################
    def is_known_system(self, system: "System") -> bool:
        """Is the system known to this empire"""
        return system.id in self.known_systems


#####################################################################################################
def make_empire(empire_name: str, empire_colour: str, home_system: "System") -> Empire:
    """ """
    home_system.colour = StarColour.YELLOW
    empire = Empire(empire_name, empire_colour)
    home_planet = make_home_planet(home_system)
    empire.set_home_planet(home_planet)
    home_system.orbits.append(home_planet)
    random.shuffle(home_system.orbits)
    return empire
