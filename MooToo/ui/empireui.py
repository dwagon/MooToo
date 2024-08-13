""" Act as a copy of the empire class for UI purposes"""

from typing import Any
from enum import StrEnum, auto

from MooToo.research import TechCategory
from MooToo.utils import SystemId, ShipId
from ui_util import get, get_cache, post
from MooToo.constants import Technology


#####################################################################################################
class CacheKeys(StrEnum):
    EMPIRE = auto()
    SHIPS = auto()
    FREIGHTERS = auto()
    FREIGHTERS_USED = auto()
    MONEY = auto()
    FOOD = auto()
    IS_KNOWN = auto()
    KNOWN_SYSTEMS = auto()


#####################################################################################################
class EmpireUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["empire"]
        self.id = data["id"]
        self.income = data["income"]
        self.money = data["money"]
        self.name = data["name"]
        self.freighters = data["freighters"]
        self.freight_used = data["freighters_used"]
        self.cache: dict[CacheKeys, Any] = {}
        self.dirty: dict[CacheKeys, bool] = {}
        self.research_cache: dict["TechCategory" : list[Technology]] = {}

    #################################################################################################
    def reset_cache(self):
        self.cache = {}
        self.dirty = {}
        self.research_cache = {}

    #################################################################################################
    def freighters_used(self):
        return self.freight_used

    #################################################################################################
    def food(self) -> int:
        return get_cache(self, CacheKeys.FOOD, "food")["food"]

    #####################################################################################################
    def is_known_system(self, system_id: SystemId) -> bool:
        return get_cache(self, CacheKeys.IS_KNOWN, f"{system_id}/is_known")["known"]

    #####################################################################################################
    @property
    def researching(self) -> Technology:
        return get_cache(self, CacheKeys.EMPIRE, "researching")["researching"]

    #####################################################################################################
    @property
    def known_systems(self) -> set[SystemId]:
        return get_cache(self, CacheKeys.KNOWN_SYSTEMS, "known_systems")["known"]

    #####################################################################################################
    @property
    def ships(self) -> list[ShipId]:
        if self.dirty.get(CacheKeys.SHIPS, True):
            ship_list = get("/ships")["ships"]
            self.cache[CacheKeys.SHIPS] = [_["id"] for _ in ship_list]
            self.dirty[CacheKeys.SHIPS] = False
        return self.cache[CacheKeys.SHIPS]

    #####################################################################################################
    def next_research(self, category: "TechCategory") -> list[Technology]:
        if category not in self.research_cache:
            ans = get(f"/empires/{self.id}/{category}/next_research")["research"]
            self.research_cache[category] = [Technology(_) for _ in ans]
        return self.research_cache[category]

    #####################################################################################################
    def has_interest_in(self, system_id: SystemId) -> bool:
        return get(f"{self.url}/{system_id}/has_interest_in")["interest"]

    #####################################################################################################
    def start_researching(self, to_research: Technology) -> None:
        post(f"{self.url}/start_researching", params={"tech": to_research})
        self.dirty[CacheKeys.EMPIRE] = True


# EOF
