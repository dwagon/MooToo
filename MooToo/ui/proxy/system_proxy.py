""" Act as a copy of the system class for UI purposes"""

from enum import StrEnum, auto
from typing import Any

from MooToo.ui.proxy.proxy_util import get
from MooToo.constants import StarColour


#####################################################################################################
class CacheKeys(StrEnum):
    SYSTEM = auto()


#####################################################################################################
class SystemProxy:
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

    #####################################################################################################
    def __repr__(self):
        return f"<SystemProxy id={self.id} {self.name}>"

    #####################################################################################################
    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        try:
            data = self.orbits[self._index]
        except IndexError as e:
            raise StopIteration from e
        self._index += 1
        return data
