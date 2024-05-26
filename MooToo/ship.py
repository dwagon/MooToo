""" ship class """

from typing import TYPE_CHECKING
from enum import StrEnum, auto

if TYPE_CHECKING:
    from MooToo.system import System


#####################################################################################################
class ShipType(StrEnum):
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
counts: dict[ShipType, int] = {
    ShipType.ColonyShip: 0,
    ShipType.OutpostShip: 0,
    ShipType.Transport: 0,
    ShipType.Frigate: 0,
    ShipType.Destroyer: 0,
    ShipType.Cruiser: 0,
    ShipType.Battleship: 0,
    ShipType.Titan: 0,
    ShipType.DoomStar: 0,
}


#####################################################################################################
class Ship:
    """Things that move"""

    def __init__(self):
        self.cost = 0
        self.space = 0
        self.name = ""
        self.location: System | tuple[int, int] = (0, 0)

    def __repr__(self):
        return f"<Ship {self.name} {self.location}>"


#####################################################################################################
class Frigate(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 25
        self.space = 25
        self.type = ShipType.Frigate
        self.name = name


#####################################################################################################
class Destroyer(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 85
        self.space = 60
        self.name = name
        self.type = ShipType.Destroyer


#####################################################################################################
class Cruiser(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 300
        self.space = 120
        self.name = name
        self.type = ShipType.Cruiser


#####################################################################################################
class Battleship(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 725
        self.space = 250
        self.name = name
        self.type = ShipType.Battleship


#####################################################################################################
class Titan(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 1800
        self.space = 500
        self.name = name
        self.type = ShipType.Titan


#####################################################################################################
class DoomStar(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 4800
        self.space = 1200
        self.name = name
        self.type = ShipType.DoomStar


#####################################################################################################
def select_ship_type_by_name(name: str) -> Ship:
    match name:
        case "Frigate":
            counts[ShipType.Frigate] += 1
            return Frigate(f"Frigate {counts[ShipType.Frigate]}")
        case "Destroyer":
            counts[ShipType.Destroyer] += 1
            return Destroyer(f"Destroyer {counts[ShipType.Destroyer]}")
        case "Cruiser":
            counts[ShipType.Cruiser] += 1
            return Cruiser(f"Cruiser {counts[ShipType.Cruiser]}")
        case "Battleship":
            counts[ShipType.Battleship] += 1
            return Battleship(f"Battleship {counts[ShipType.Battleship]}")
        case "Titan":
            counts[ShipType.Titan] += 1
            return Titan(f"Titan {counts[ShipType.Titan]}")
        case "DoomStar":
            counts[ShipType.DoomStar] += 1
            return DoomStar(f"DoomStar {counts[ShipType.DoomStar]}")
        case _:
            raise NotImplementedError(f"Unhandled ship type {name=}")
