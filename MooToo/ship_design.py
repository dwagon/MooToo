""" Ship Design """

import random
from enum import StrEnum, auto
from typing import Optional

from MooToo.component import ShipComponent


#####################################################################################################
class HullType(StrEnum):
    Unknown = auto()
    ColonyBase = auto()
    ColonyShip = auto()
    OutpostShip = auto()
    Transport = auto()
    Frigate = auto()
    Destroyer = auto()
    Cruiser = auto()
    Battleship = auto()
    Titan = auto()
    DoomStar = auto()


#####################################################################################################
class HullDetails(StrEnum):
    """Keys for the HULL_SIZES dictionary"""

    Cost = auto()
    Space = auto()
    IconRange = auto()
    IconName = auto()


#####################################################################################################
HULL_SIZES = {
    HullType.ColonyShip: {
        HullDetails.Cost: 100,  # ?
        HullDetails.Space: 0,
        HullDetails.IconRange: 0,
        HullDetails.IconName: "colony",
    },
    HullType.Transport: {
        HullDetails.Cost: 25,  # ?
        HullDetails.Space: 0,
        HullDetails.IconRange: 0,
        HullDetails.IconName: "transport",
    },
    HullType.Frigate: {
        HullDetails.Cost: 25,
        HullDetails.Space: 25,
        HullDetails.IconRange: 7,
        HullDetails.IconName: "frigate",
    },
    HullType.Destroyer: {
        HullDetails.Cost: 85,
        HullDetails.Space: 60,
        HullDetails.IconRange: 7,
        HullDetails.IconName: "destroyer",
    },
    HullType.Cruiser: {
        HullDetails.Cost: 300,
        HullDetails.Space: 120,
        HullDetails.IconRange: 7,
        HullDetails.IconName: "cruiser",
    },
    HullType.Battleship: {
        HullDetails.Cost: 725,
        HullDetails.Space: 250,
        HullDetails.IconRange: 7,
        HullDetails.IconName: "battleship",
    },
    HullType.Titan: {
        HullDetails.Cost: 1800,
        HullDetails.Space: 500,
        HullDetails.IconRange: 7,
        HullDetails.IconName: "titan",
    },
    HullType.DoomStar: {
        HullDetails.Cost: 4800,
        HullDetails.Space: 1200,
        HullDetails.IconRange: 3,
        HullDetails.IconName: "doomstar",
    },
}


#####################################################################################################
class ShipDesign:
    def __init__(self, hull: HullType, name=""):
        self.id: Optional[int] = None
        self.name = name
        self.space = 0
        self.cost = 0
        self.hull: HullType = hull
        self.shield = None
        self.computer = None
        self.components: list["ShipComponent"] = []
        self._icon_number = random.randint(0, HULL_SIZES[self.hull][HullDetails.IconRange])

    #################################################################################################
    def __repr__(self):
        return f"<ShipDesign '{self.name}' {self.hull}>"

    #################################################################################################
    def cost(self) -> int:
        return HULL_SIZES[self.hull][HullDetails.Cost] + sum(_.cost for _ in self.components)

    #################################################################################################
    @property
    def icon(self) -> str:
        if HULL_SIZES[self.hull][HullDetails.IconRange]:
            return f"{HULL_SIZES[self.hull][HullDetails.IconName]}_{self._icon_number}"
        return HULL_SIZES[self.hull][HullDetails.IconName]


# EOF
