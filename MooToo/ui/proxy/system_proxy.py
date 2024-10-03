""" Act as a copy of the system class for UI purposes"""

import requests
from enum import StrEnum, auto
from typing import Any

from MooToo.ui.proxy.proxy_util import Proxy
from MooToo.constants import StarColour


#####################################################################################################
class CacheKeys(StrEnum):
    SYSTEM = auto()


#####################################################################################################
class SystemProxy(Proxy):
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        self.url = url
        data = self.get(self.url)["system"]
        self.id = data["id"]
        self.position = (data["position"]["x"], data["position"]["y"])
        self.name = data["name"]
        self.orbits = data["orbits"]
        self.planets = data["planets"]
        self.colour = StarColour(data["colour"].lower())

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


# EOF
