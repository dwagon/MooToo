""" Relating to player's empires"""

from MooToo.system import System, StarColour
from MooToo.planet import Planet, PopulationJobs
from MooToo.config import Config


class Empire:
    def __init__(self, name: str, home_planet: System, config: Config):
        self.name = name
        self.config = config
        self.home_planet = home_planet
        self.home_planet.draw_colour = "Green"

    def make_home_planet(self, orbit: int) -> Planet:
        """Return a suitable home planet"""
        p = Planet(f"{self.name} Home", orbit, self.config["galaxy"]["star_colours"][StarColour.YELLOW])
        p.make_home_world()
        p.owner = self
        p.population[PopulationJobs.FARMER] = 2
        p.population[PopulationJobs.WORKERS] = 2
        p.population[PopulationJobs.SCIENTISTS] = 2
        return p
