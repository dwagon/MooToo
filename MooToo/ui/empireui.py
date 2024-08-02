""" Act as a copy of the empire class for UI purposes"""

from typing import TYPE_CHECKING
from ui_util import get
from MooToo.constants import Technology
from MooToo.ui.shipui import ShipUI as Ship


if TYPE_CHECKING:
    from MooToo.ui.systemui import SystemUI as System


#####################################################################################################
class EmpireUI:
    def __init__(self, url: str):
        self.url = url
        data = get(url)["empire"]
        self.id = data["id"]
        self.income = data["income"]

    #################################################################################################
    @property
    def money(self) -> int:
        data = get(self.url)["empire"]
        return data["money"]

    #################################################################################################
    @property
    def freighters(self) -> int:
        data = get(self.url)["empire"]
        return data["freighters"]

    #################################################################################################
    def freighters_used(self) -> int:
        data = get(self.url)["empire"]
        return data["freighters_used"]

    #################################################################################################
    def food(self) -> int:
        return get(f"/empires/{self.id}/food")["food"]

    #####################################################################################################
    def is_known_system(self, system: "System") -> bool:
        return get(f"/empires/{self.id}/{system.id}/is_known")["known"]

    #####################################################################################################
    @property
    def researching(self) -> Technology:
        return get(f"/empires/{self.id}/researching")["researching"]

    #####################################################################################################
    @property
    def ships(self) -> list["Ship"]:
        ship_list = get(f"/empires/{self.id}/ships")["ships"]
        return [Ship(_["url"]) for _ in ship_list]
