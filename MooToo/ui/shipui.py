""" Act as a copy of the ship class for UI purposes"""

from enum import StrEnum, auto
from typing import Optional, Any

from MooToo.utils import SystemId
from .ui_util import get, post, get_cache
from .systemui import SystemUI as System


#####################################################################################################
class CacheKeys(StrEnum):
    SHIP = auto()


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
        return get_cache(self, CacheKeys.SHIP)["ship"]["destination"]

    #################################################################################################
    def set_destination(self, dest_system: "System") -> None:
        post(f"/ships/{self.id}/set_destination", {"dest_system": dest_system})
