""" Act as a copy of the design class for UI purposes"""

import requests
from enum import StrEnum, auto
from MooToo.ui.proxy.proxy_util import Proxy


#####################################################################################################
class CacheKeys(StrEnum):
    SHIP = auto()


#####################################################################################################
class ShipDesignProxy(Proxy):
    def __init__(self, url: str, getter=requests.get, poster=requests.post):
        super().__init__(url, getter, poster)
        data = self.get(self.url)["design"]
        self.id = data["id"]
        self.hull = data["hull"]


# EOF
