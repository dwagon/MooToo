""" Act as a copy of the planet class for UI purposes"""

from enum import StrEnum, auto
from typing import Any

from MooToo.constants import PlanetClimate, PlanetCategory, PlanetRichness, PlanetSize, PlanetGravity
from .ui_util import get, get_cache


#####################################################################################################
class CacheKeys(StrEnum):
    PLANET = auto()
    ARC = auto()
    MAX_POP = auto()


#####################################################################################################
class PlanetUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["planet"]
        self.id = data["id"]
        self.name = data["name"]
        self.size = PlanetSize(data["size"])
        self.category = PlanetCategory(data["category"])
        self.climate = PlanetClimate(data["climate"])
        self.richness = PlanetRichness(data["richness"])
        self.gravity = PlanetGravity(data["gravity"])

        self.cache: dict[CacheKeys, Any] = {}
        self.dirty: dict[CacheKeys, bool] = {}

    #################################################################################################
    @property
    def arc(self) -> int:
        return get_cache(self, CacheKeys.ARC)["planet"]["arc"]

    #################################################################################################
    def max_population(self) -> int:
        return get_cache(self, CacheKeys.MAX_POP)["planet"]["max_pop"]


# EOF
