""" Act as a copy of the ship class for UI purposes"""

from enum import StrEnum, auto
from typing import Optional, Any

from .ui_util import get, post
from .systemui import SystemUI as System


#####################################################################################################
class CacheKeys(StrEnum):
    ORBIT = auto()
    DESTINATION = auto()


#####################################################################################################
class ShipUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["ship"]
        self.id = data["id"]
        self.name = data["name"]
        self.icon = data["icon"]
        self.cache: dict[CacheKeys, Any] = {}

    #################################################################################################
    def load_cache(self):
        self.cache[CacheKeys.ORBIT] = None
        self.cache[CacheKeys.DESTINATION] = None

    #################################################################################################
    @property
    def orbit(self) -> Optional[System]:
        if not self.cache.get(CacheKeys.ORBIT):
            data = get(self.url)["ship"]
            if data["orbit"]:
                self.cache[CacheKeys.ORBIT] = System(data["orbit"]["url"])
        return self.cache[CacheKeys.ORBIT]

    #################################################################################################
    @property
    def destination(self) -> Optional[System]:
        try:
            if not self.cache[CacheKeys.DESTINATION]:
                data = get(self.url)["ship"]
                if data["destination"]:
                    self.cache[CacheKeys.DESTINATION] = System(data["destination"]["url"])
        except KeyError:
            return self.cache[CacheKeys.DESTINATION]

    #################################################################################################
    def set_destination(self, dest_system: "System") -> None:
        post("/ship/{ship.id}/set_destination", {"dest_system": dest_system})
