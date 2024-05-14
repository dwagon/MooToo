""" Relating to player's empires"""

from MooToo.system import System, StarColour
from MooToo.planet import Planet, PopulationJobs
from MooToo.config import Config
from MooToo import building


#####################################################################################################
#####################################################################################################
class Empire:
    def __init__(self, name: str, home_planet: System, config: Config):
        self.name = name
        self.config = config
        self.government = "Feudal"  # Fix me
        self.home_planet = home_planet
        self.money = 100
        self.known: dict[System, bool] = {}

    #####################################################################################################
    def know(self, system: System) -> None:
        self.known[system] = True

    #####################################################################################################
    def is_known(self, system: System) -> bool:
        """Is the system known to this empire"""
        return system in self.known

    #####################################################################################################

    def make_home_planet(self, orbit: int) -> Planet:
        """Return a suitable home planet"""
        p = Planet(f"{self.name} Home", orbit, self.config["galaxy"]["star_colours"][StarColour.YELLOW])
        p.make_home_world()
        p.owner = self
        p.population = 8e6
        p.jobs[PopulationJobs.FARMER] = 4
        p.jobs[PopulationJobs.WORKERS] = 2
        p.jobs[PopulationJobs.SCIENTISTS] = 2
        p.buildings["Hydroponic Farm"] = building.HydroponicFarm()
        p.under_construction = building.AutomatedFactory()
        p.gen_climate_image()
        return p
