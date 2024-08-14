""" Act as a copy of the planet class for UI purposes"""

from enum import StrEnum, auto
from typing import Any

from MooToo.constants import PlanetClimate, PlanetCategory, PlanetRichness, PlanetSize, PlanetGravity, PopulationJobs
from .ui_util import get, get_cache
from ..utils import PlanetId
from MooToo.utils import get_building


#####################################################################################################
class CacheKeys(StrEnum):
    PLANET = auto()
    ARC = auto()
    MAX_POP = auto()
    POP_INCR = auto()
    POPULATION = auto()


#####################################################################################################
class PlanetUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["planet"]
        self.id = data["id"]
        self.name = data["name"]
        self.owner = data["owner"]
        self.size = PlanetSize(data["size"])
        self.category = PlanetCategory(data["category"])
        self.climate = PlanetClimate(data["climate"])
        self.richness = PlanetRichness(data["richness"])
        self.gravity = PlanetGravity(data["gravity"])
        self.buildings = data["buildings"]
        self.climate_image = data["climate_image"]
        self.system_id = data["system_id"]
        self.jobs = {
            PopulationJobs.FARMERS: data["jobs"][PopulationJobs.FARMERS],
            PopulationJobs.WORKERS: data["jobs"][PopulationJobs.WORKERS],
            PopulationJobs.SCIENTISTS: data["jobs"][PopulationJobs.SCIENTISTS],
        }
        self.build_queue = []

        self.cache: dict[CacheKeys, Any] = {}
        self.dirty: dict[CacheKeys, bool] = {}

    #####################################################################################################
    def __getitem__(self, item):
        return get_building(item)

    #################################################################################################
    @property
    def arc(self) -> int:
        return get_cache(self, CacheKeys.ARC)["planet"]["arc"]

    #################################################################################################
    def max_population(self) -> int:
        return get_cache(self, CacheKeys.MAX_POP)["planet"]["max_pop"]

    #################################################################################################
    def morale(self) -> int:
        return get_cache(self, CacheKeys.PLANET)["planet"]["morale"]

    #################################################################################################
    def current_population(self) -> int:
        return get_cache(self, CacheKeys.PLANET)["planet"]["population"]

    #################################################################################################
    @property
    def raw_population(self) -> int:
        return get_cache(self, CacheKeys.PLANET)["planet"]["raw_population"]

    #################################################################################################
    def population_increment(self) -> int:
        return get_cache(self, CacheKeys.PLANET)["planet"]["population_increment"]


#################################################################################################
def money_production(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["money_production"]


#################################################################################################
def money_cost(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["money_cost"]


#################################################################################################
def food_per(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["food_per"]


#################################################################################################
def food_cost(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["food_cost"]


#################################################################################################
def food_surplus(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["food_surplus"]


#################################################################################################
def work_per(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["work_per"]


#################################################################################################
def work_cost(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["work_cost"]


#################################################################################################
def work_surplus(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["work_surplus"]


#################################################################################################
def science_per(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["science_per"]


#################################################################################################
def science_production(planet_id: PlanetId) -> int:
    return get(f"/planets/{planet_id}")["planet"]["science_production"]


# EOF
