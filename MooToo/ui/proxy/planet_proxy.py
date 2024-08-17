""" Act as a copy of the planet class for UI purposes"""

from enum import StrEnum, auto
from typing import Any

from MooToo.constants import (
    PlanetClimate,
    PlanetCategory,
    PlanetRichness,
    PlanetSize,
    PlanetGravity,
    PopulationJobs,
    Building,
)
from MooToo.ui.proxy.proxy_util import get, get_cache, post
from MooToo.utils import get_building


#####################################################################################################
class CacheKeys(StrEnum):
    PLANET = auto()
    ARC = auto()
    MAX_POP = auto()
    POP_INCR = auto()
    POPULATION = auto()


#####################################################################################################
class PlanetProxy:
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
        self.money_production = data["money_production"]
        self.money_cost = data["money_cost"]
        self.food_per = data["food_per"]
        self.food_cost = data["food_cost"]
        self.food_surplus = data["food_surplus"]
        self.work_per = data["work_per"]
        self.work_cost = data["work_cost"]
        self.work_surplus = data["work_surplus"]
        self.science_per = data["science_per"]
        self.science_production = data["science_production"]

        self._jobs = {
            PopulationJobs.FARMERS: data["jobs"][PopulationJobs.FARMERS],
            PopulationJobs.WORKERS: data["jobs"][PopulationJobs.WORKERS],
            PopulationJobs.SCIENTISTS: data["jobs"][PopulationJobs.SCIENTISTS],
        }
        self.build_queue = []

        self.cache: dict[CacheKeys, Any] = {}
        self.dirty: dict[CacheKeys, bool] = {}

    #################################################################################################
    def reset_cache(self):
        self.dirty: dict[CacheKeys, bool] = {}

    #################################################################################################
    @property
    def jobs(self):
        return get_cache(self, CacheKeys.PLANET)["planet"]["jobs"]

    #################################################################################################
    @property
    def buildings_available(self) -> set[Building]:
        pass

    #################################################################################################
    def __getitem__(self, item):
        return get_building(item)

    #####################################################################################################
    def buy_cost(self) -> int:
        pass

    #####################################################################################################
    def turns_to_build(self) -> int:
        pass

    #####################################################################################################
    def available_to_build(self) -> set[Building]:
        pass

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

    #####################################################################################################
    def move_workers(self, num: int, src_job: PopulationJobs, target_job: PopulationJobs):
        self.reset_cache()
        return post(f"{self.url}/move_workers", params={"num": num, "src_job": src_job, "target_job": target_job})


# EOF
