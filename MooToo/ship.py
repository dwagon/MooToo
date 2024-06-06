""" ship class """

import math
import random

from typing import TYPE_CHECKING, Optional
from enum import StrEnum, auto
from MooToo.utils import get_distance_tuple

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
        self.command_points = 0
        self.maintenance = 0
        self.name = ""
        self.icon = ""
        self.destination: Optional[System] = None
        self.location: tuple[int, int] = (-1, -1)
        self.orbit: Optional[System] = None

    #################################################################################################
    def __repr__(self):
        if self.orbit:
            return f"<Ship {self.name} {self.orbit}>"
        else:
            return f"<Ship {self.name} {self.location}>"

    #################################################################################################
    def speed(self):
        """How fast the ship moves"""
        return 2

    #################################################################################################
    def set_destination(self, system: "System") -> None:
        if self.orbit:
            self.location = self.orbit.position
        self.destination = system

    #################################################################################################
    def arrived_at_destination(self):
        self.orbit = self.destination
        self.location = self.destination.position
        self.destination = None

    #################################################################################################
    def move_towards_destination(self):
        if get_distance_tuple(self.location, self.destination.position) < self.speed() + 0.01:
            self.arrived_at_destination()

            return
        angle = math.atan2(
            self.destination.position[1] - self.location[1], self.destination.position[0] - self.location[0]
        )
        self.location = (
            int(self.location[0] + math.cos(angle) * self.speed()),
            int(self.location[1] + math.sin(angle) * self.speed()),
        )
        self.orbit = None

    #################################################################################################
    def turn(self):
        """Have a turn"""
        if self.destination:
            self.move_towards_destination()


#####################################################################################################
class Transport(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 25  # ?
        self.space = 0
        self.command_points = 1
        self.maintenance = 10
        self.type = ShipType.Transport
        self.name = name
        self.icon = "transport"


#####################################################################################################
class Frigate(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 25
        self.space = 25
        self.type = ShipType.Frigate
        self.name = name
        self.icon = f"frigate_{random.randint(0, 7)}"


#####################################################################################################
class Destroyer(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 85
        self.space = 60
        self.name = name
        self.type = ShipType.Destroyer
        self.icon = f"destroyer_{random.randint(0, 7)}"


#####################################################################################################
class Cruiser(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 300
        self.space = 120
        self.name = name
        self.type = ShipType.Cruiser
        self.icon = f"cruiser_{random.randint(0, 7)}"


#####################################################################################################
class Battleship(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 725
        self.space = 250
        self.name = name
        self.type = ShipType.Battleship
        self.icon = f"battleship_{random.randint(0, 7)}"


#####################################################################################################
class Titan(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 1800
        self.space = 500
        self.name = name
        self.type = ShipType.Titan
        self.icon = f"titan_{random.randint(0, 7)}"


#####################################################################################################
class DoomStar(Ship):
    def __init__(self, name: str):
        super().__init__()
        self.cost = 4800
        self.space = 1200
        self.name = name
        self.type = ShipType.DoomStar
        self.icon = f"doomstar_{random.randint(0, 3)}"


#####################################################################################################
def select_ship_type_by_name(name: str) -> Ship:
    match name:
        case "Transport":
            counts[ShipType.Transport] += 1
            return Transport(f"Transport {counts[ShipType.Transport]:03d}")
        case "Frigate":
            counts[ShipType.Frigate] += 1
            return Frigate(f"Frigate {counts[ShipType.Frigate]:03d}")
        case "Destroyer":
            counts[ShipType.Destroyer] += 1
            return Destroyer(f"Destroyer {counts[ShipType.Destroyer]:03d}")
        case "Cruiser":
            counts[ShipType.Cruiser] += 1
            return Cruiser(f"Cruiser {counts[ShipType.Cruiser]:03d}")
        case "Battleship":
            counts[ShipType.Battleship] += 1
            return Battleship(f"Battleship {counts[ShipType.Battleship]:03d}")
        case "Titan":
            counts[ShipType.Titan] += 1
            return Titan(f"Titan {counts[ShipType.Titan]:03d}")
        case "DoomStar":
            counts[ShipType.DoomStar] += 1
            return DoomStar(f"DoomStar {counts[ShipType.DoomStar]:03d}")
        case _:
            raise NotImplementedError(f"Unhandled ship type {name=}")
