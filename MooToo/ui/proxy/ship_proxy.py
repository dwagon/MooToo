""" Act as a copy of the ship class for UI purposes"""

import requests
from enum import StrEnum, auto
from typing import Optional

from MooToo.utils import SystemId
from MooToo.ui.proxy.proxy_util import Proxy


#####################################################################################################
class CacheKeys(StrEnum):
    SHIP = auto()
    LOCATION = auto()


#####################################################################################################
class ShipProxy(Proxy):
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        data = self.get(self.url)["ship"]
        self.id = data["id"]
        self.name = data["name"]
        self.icon = data["icon"]
        self.coloniser = data["coloniser"]
        self.target_planet_id = data["target_planet_id"]

    #################################################################################################
    def __repr__(self):
        if self.orbit:
            return f"<ShipProxy {self.id} '{self.name}' {self.orbit}>"
        else:
            return f"<ShipProxy {self.id} '{self.name}' {self.location}>"

    #################################################################################################
    @property
    def orbit(self) -> Optional[SystemId]:
        if orbit := self.get_cache(CacheKeys.SHIP)["ship"]["orbit"]:
            return orbit

    #################################################################################################
    @property
    def destination(self) -> Optional[SystemId]:
        if dest := self.get_cache(CacheKeys.SHIP)["ship"]["destination"]:
            return dest
        return None

    #################################################################################################
    @property
    def location(self) -> tuple[int, int]:
        data = self.get_cache(CacheKeys.LOCATION)["ship"]
        return data["location_id"]

    #################################################################################################
    def speed(self) -> int:
        return self.get_cache(CacheKeys.SHIP)["ship"]["speed"]

    #################################################################################################
    def set_destination(self, dest_system_id: SystemId) -> SystemId:
        self.post(f"/ships/{self.id}/set_destination", params={"destination_id": dest_system_id})
        self.reset_cache()
        return self.destination
