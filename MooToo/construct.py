""" Things that can be built - ships & buildings"""

from enum import StrEnum, auto

from typing import Optional, TYPE_CHECKING
from MooToo.utils import get_building, DesignId

if TYPE_CHECKING:
    from MooToo.planet_building import Building
    from MooToo.galaxy import Galaxy


#########################################################################################################
class ConstructType(StrEnum):
    BUILDING = auto()
    SHIP = auto()
    COLONY_BASE = auto()
    COLONY_SHIP = auto()
    TRANSPORT = auto()
    FREIGHTER = auto()
    SPY = auto()


#########################################################################################################
class Construct:
    def __init__(
        self,
        category: ConstructType,
        building_tag: Optional["Building"] = None,
        design_id: Optional["DesignId"] = None,
    ):

        self._cost = 0
        self.category = category
        self.design_id = design_id
        self.building_tag = building_tag

    #############################################################################################
    def __hash__(self):
        return hash(self.category) + hash(self.design_id) + hash(self.building_tag)

    #############################################################################################
    def name(self, galaxy: Optional["Galaxy"]) -> str:
        match self.category:
            case ConstructType.SHIP:
                return galaxy.designs[self.design_id].name
            case ConstructType.FREIGHTER:
                return "Freighter Fleet"
            case ConstructType.SPY:
                return "Spy"
            case ConstructType.COLONY_BASE:
                return "Colony Base"
            case _:
                return self.building_tag.name.title()

    #############################################################################################
    def __str__(self):
        if self.category == ConstructType.SHIP:
            return f"<Construct ship={self.name}>"
        else:
            return f"<Construct building={self.name}>"

    #############################################################################################
    def __eq__(self, other):
        if not isinstance(other, Construct):
            return False
        if self.category == ConstructType.BUILDING:
            return self.category == other.category and self.building_tag == other.building_tag
        return False

    #############################################################################################
    def cost(self, galaxy: Optional["Galaxy"]) -> int:
        match self.category:
            case ConstructType.SHIP:
                return galaxy.designs[self.design_id].cost
            case ConstructType.BUILDING:
                return get_building(self.building_tag).cost
            case ConstructType.FREIGHTER:
                return 50
            case ConstructType.SPY:
                return 100
            case ConstructType.COLONY_BASE:
                return 200


# EOF
