""" Act as a copy of the empire class for UI purposes"""

from enum import StrEnum, auto
from typing import Optional

import requests

from MooToo.research import TechCategory
from MooToo.utils import SystemId, ShipId, PlanetId
from MooToo.ui.proxy.proxy_util import Proxy
from MooToo.constants import Technology, PopulationJobs


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
class EmpireProxy(Proxy):
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        data = self.get(self.url)["empire"]
        self.id = data["id"]
        self.colour = data["colour"]
        self.income = data["income"]
        self.government = data["government"]
        self.money = data["money"]
        self.name = data["name"]
        self.known_systems = data["known_systems"]
        self.research_spent = data["research_spent"]
        self.owned_planets = data["owned_planets"]
        self.research_points = data["research_points"]
        self.freighters = data["freighters"]
        self.freight_used = data["freighters_used"]
        self.research_cache: dict["TechCategory" : list[Technology]] = {}
        self.reset_cache()

    #################################################################################################
    def reset_cache(self):
        super().reset_cache()
        self.research_cache = {}

    #################################################################################################
    def freighters_used(self):
        return self.freight_used

    #################################################################################################
    def food(self) -> int:
        return self.get_cache(CacheKeys.FOOD, "food")["food"]

    #####################################################################################################
    def is_known_system(self, system_id: SystemId) -> bool:
        return system_id in self.known_systems

    #####################################################################################################
    @property
    def researching(self) -> Technology:
        return self.get_cache(CacheKeys.EMPIRE, "researching")["researching"]

    #####################################################################################################
    @property
    def ships(self) -> list[ShipId]:
        if self.dirty.get(CacheKeys.SHIPS, True):
            ship_list = self.get("/ships")["ships"]
            self.cache[CacheKeys.SHIPS] = [_["id"] for _ in ship_list]
            self.dirty[CacheKeys.SHIPS] = False
        return self.cache[CacheKeys.SHIPS]

    #####################################################################################################
    def next_research(self, category: "TechCategory") -> list[Technology]:
        if category not in self.research_cache:
            ans = self.get(f"/empires/{self.id}/{category}/next_research")["research"]
            self.research_cache[category] = [Technology(_) for _ in ans]
        return self.research_cache[category]

    #####################################################################################################
    def has_interest_in(self, system_id: SystemId) -> bool:
        return self.get(f"{self.url}/{system_id}/has_interest_in")["interest"]

    #####################################################################################################
    def start_researching(self, to_research: Technology) -> None:
        self.post(f"{self.url}/start_researching", params={"tech": to_research})
        self.dirty[CacheKeys.EMPIRE] = True

    #####################################################################################################
    def get_research_points(self) -> int:
        return self.research_points

    #####################################################################################################
    def send_coloniser(self, dest_planet_id: PlanetId) -> Optional[ShipId]:
        data = self.post(f"{self.url}/send_coloniser", params={"dest_planet_id": dest_planet_id})
        coloniser = data["ship"]
        self.reset_cache()
        return coloniser

    #####################################################################################################
    def migrate(
        self,
        num: int,
        src_planet_id: PlanetId,
        src_job: PopulationJobs,
        dst_planet_id: PlanetId,
        dst_job: PopulationJobs,
    ):
        self.post(
            f"{self.url}/migrate",
            params={
                "num": num,
                "src_planet_id": src_planet_id,
                "src_job": src_job,
                "dst_planet_id": dst_planet_id,
                "dst_job": dst_job,
            },
        )
        self.reset_cache()


# EOF
