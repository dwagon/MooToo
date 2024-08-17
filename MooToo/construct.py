""" Things that can be built - ships & buildings"""

from enum import StrEnum, auto

from typing import Optional, TYPE_CHECKING
from MooToo.utils import get_building

if TYPE_CHECKING:
    from MooToo.planet_building import Building
    from MooToo.ship import Ship


#########################################################################################################
class ConstructType(StrEnum):
    BUILDING = auto()
    SHIP = auto()
    COLONY_BASE = auto()
    FREIGHTER = auto()
    SPY = auto()


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
    @property
    def name(self) -> str:
        match self.category:
            case ConstructType.SHIP:
                return self.ship.name
            case ConstructType.FREIGHTER:
                return "Freighter Fleet"
            case ConstructType.SPY:
                return "Spy"
            case ConstructType.COLONY_BASE:
                return "Colony Base"
            case _:
                return self.tag.name.title()

    #############################################################################################
    def __str__(self):
        if self.category == ConstructType.SHIP:
            return f"<Construct ship={self.ship}>"
        else:
            return f"<Construct building={self.tag.name}>"

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
        match self.category:
            case ConstructType.SHIP:
                return self.ship.cost
            case ConstructType.BUILDING:
                return get_building(self.tag).cost
            case ConstructType.FREIGHTER:
                return 50
            case ConstructType.SPY:
                return 100
            case ConstructType.COLONY_BASE:
                return 200
