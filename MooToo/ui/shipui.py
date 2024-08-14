""" Act as a copy of the ship class for UI purposes"""

from enum import StrEnum, auto
from typing import Optional, Any

from MooToo.utils import SystemId
from .ui_util import get, post, get_cache


#####################################################################################################
class CacheKeys(StrEnum):
    SHIP = auto()
    LOCATION = auto()


#####################################################################################################
class ShipUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["ship"]
        self.id = data["id"]
        self.name = data["name"]
        self.icon = data["icon"]
        self.cache: dict[CacheKeys, Any] = {}
        self.dirty: dict[CacheKeys, bool] = {}

    #################################################################################################
    @property
    def orbit(self) -> Optional[SystemId]:
        if orbit := get_cache(self, CacheKeys.SHIP)["ship"]["orbit"]:
            return orbit["id"]

    #################################################################################################
    @property
    def destination(self) -> Optional[SystemId]:
        dest = get_cache(self, CacheKeys.SHIP)["ship"]["destination"]
        if dest:
            print(f"destination {dest=}")
        return dest

    #################################################################################################
    @property
    def location(self) -> tuple[int, int]:
        dest = get_cache(self, CacheKeys.LOCATION)["ship"]["location"]
        print(f"location {dest=}")
        return dest

    #################################################################################################
    def set_destination(self, dest_system_id: SystemId) -> SystemId:
        post(f"/ships/{self.id}/set_destination", params={"destination_id": dest_system_id})
        return self.destination
