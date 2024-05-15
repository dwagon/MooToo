""" Relating to player's empires"""

from typing import TYPE_CHECKING

from MooToo.system import System, StarColour
from MooToo.planet import Planet, PopulationJobs
from MooToo.config import Config
from MooToo.research import Research
from MooToo.researches.AdvancedConstruction import ResearchAutomatedFactory

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, name: str, home_planet: System, galaxy: "Galaxy", config: Config):
        self.name = name
        self.galaxy = galaxy
        self.config = config
        self.government = "Feudal"  # Fix me
        self.home_planet = home_planet
        self.money = 100
        self.known_systems: dict[System, bool] = {}  # Known systems
        self.owned_planets: list[Planet] = []  # Owned planets
        self.researching = ResearchAutomatedFactory()
        self.research_spent = 0
        self.techs: dict[str, Research] = {}

    #####################################################################################################
    def turn(self):
        """Have a turn"""
        for planet in self.owned_planets:
            planet.turn()
        self.research_spent += self.get_research_points()
        if self.researching and self.research_spent > self.researching.cost:
            self.techs[self.researching.name] = self.researching
            self.researching = None

    #####################################################################################################
    def get_research_points(self) -> int:
        rp = 0
        for planet in self.owned_planets:
            rp += planet.get_research_points()
        return rp

    #####################################################################################################
    def know_system(self, system: System) -> None:
        self.known_systems[system] = True

    #####################################################################################################
    def is_known_system(self, system: System) -> bool:
        """Is the system known to this empire"""
        return system in self.known_systems

    #####################################################################################################

    def make_home_planet(self, orbit: int) -> Planet:
        """Return a suitable home planet"""
        p = Planet(f"{self.name} Home", orbit, self.config["galaxy"]["star_colours"][StarColour.YELLOW])
        p.make_home_world()
        p.owner = self
        self.owned_planets.append(p)
        p.population = 8e6
        p.jobs[PopulationJobs.FARMER] = 4
        p.jobs[PopulationJobs.WORKERS] = 2
        p.jobs[PopulationJobs.SCIENTISTS] = 2
        p.build_queue = []
        p.gen_climate_image()
        return p
