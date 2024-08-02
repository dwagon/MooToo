""" Act as a copy of the ship class for UI purposes"""

from typing import Optional

from .ui_util import get
from .systemui import SystemUI as System


#####################################################################################################
class ShipUI:
    def __init__(self, url: str):
        self.url = url
        data = get(self.url)["ship"]
        self.id = data["id"]
        self.name = data["name"]

    #################################################################################################
    @property
    def orbit(self) -> Optional[System]:
        data = get(self.url)["ship"]
        if data["orbit"]:
            return System(data["orbit"]["url"])

    #################################################################################################
    @property
    def destination(self) -> Optional[System]:
        data = get(self.url)["ship"]
        if data["destination"]:
            return System(data["destination"]["url"])
