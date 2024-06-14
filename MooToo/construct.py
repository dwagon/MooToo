""" Things that can be built - ships & buildings"""

from enum import Enum, auto

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo import Building, Ship, _buildings


#########################################################################################################
class ConstructType(Enum):
    BUILDING = auto()
    SHIP = auto()


#########################################################################################################
class Construct:
    def __init__(
        self, category: ConstructType, building_tag: Optional["Building"] = None, ship: Optional["Ship"] = None
    ):

        self._cost = 0
        self.category = category
        self.ship = ship
        self.tag = building_tag

    #############################################################################################
    def __repr__(self):
        if self.category == ConstructType.SHIP:
            return f"<Construct {self.category} {self.ship}>"
        else:
            return f"<Construct {self.category} {self.tag.name}>"

    #############################################################################################
    def __eq__(self, other):
        if not isinstance(other, Construct):
            return False
        if self.category == ConstructType.BUILDING:
            return self.category == other.category and self.tag == other.tag
        return False

    #############################################################################################
    @property
    def cost(self) -> int:
        if self.category == ConstructType.SHIP:
            return self._cost
        else:
            return _buildings[self.tag]._cost

    @cost.setter
    def cost(self, value: int):
        self._cost = value


########################################################################################################
