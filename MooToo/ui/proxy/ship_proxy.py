""" Act as a copy of the ship class for UI purposes"""

import requests
from enum import StrEnum, auto
from typing import Optional, TYPE_CHECKING

from MooToo.ship_design import HullType
from MooToo.ui.proxy.design_proxy import ShipDesignProxy
from MooToo.utils import SystemId
from MooToo.ui.proxy.proxy_util import Proxy

if TYPE_CHECKING:
    from MooToo.ui.proxy.galaxy_proxy import GalaxyProxy


#####################################################################################################
class CacheKeys(StrEnum):
    SHIP = auto()
    LOCATION = auto()


#####################################################################################################
class ShipProxy(Proxy):
    def __init__(self, url: str, galaxy: "GalaxyProxy", getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        data = self.get(self.url)["ship"]
        self.galaxy = galaxy
        self.id = data["id"]
        self.owner = data["owner"]
        self.design_id = data["design_id"]
        self.name = data["name"]
        self.icon = data["icon"]
        self.range = data["range"]
        self.target_planet_id = data["target_planet_id"]

    #################################################################################################
    def __repr__(self):
        if self.orbit:
            return f"<ShipProxy {self.id}@{self.owner} '{self.name}' {self.orbit}>"
        else:
            return f"<ShipProxy {self.id}@{self.owner} '{self.name}' {self.location} -> {self.destination}>"

    #################################################################################################
    @property
    def design(self) -> ShipDesignProxy:
        return self.galaxy.designs[self.design_id]

    #################################################################################################
    @property
    def coloniser(self) -> bool:
        return self.design.hull == HullType.ColonyShip

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
