""" Act as a copy of the system class for UI purposes"""

from enum import StrEnum, auto
from typing import Any

from MooToo.ui.ui_util import get, get_cache
from MooToo.constants import StarColour


#####################################################################################################
class CacheKeys(StrEnum):
    SYSTEM = auto()


#####################################################################################################
class SystemUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["system"]
        self.id = data["id"]
        self.position = (data["position"]["x"], data["position"]["y"])
        self.name = data["name"]
        self.orbits = data["orbits"]
        self.colour = StarColour(data["colour"].lower())
        self.cache: dict[CacheKeys, Any] = {}
        self.dirty: dict[CacheKeys, bool] = {}
