""" ship class """

import math
import random

from typing import TYPE_CHECKING, Optional
from enum import StrEnum, auto

from MooToo.utils import get_distance_tuple, ShipId, EmpireId, SystemId, PlanetId
from MooToo.constants import PlanetCategory


if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
class ShipType(StrEnum):
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

    def __init__(self, name: str, galaxy: "Galaxy"):
        self.galaxy = galaxy
        self.id: ShipId = next(galaxy.ship_id_generator)
        self.space = 0
        self.cost = 0
        self.space = 0
        self.owner: EmpireId = 0
        self.command_points = 0
        self.maintenance = 0
        self.coloniser = False
        self.name = name
        self.icon = ""
        self.destination: Optional[SystemId] = None
        self.location: tuple[int, int] = (-1, -1)
        self.orbit: Optional[SystemId] = None
        self.type = ShipType.Unknown

    #################################################################################################
    def built(self) -> bool:
        """Just been built; return False to delete on build"""
        return True

    #################################################################################################
    def __repr__(self):
        if self.orbit:
            return f"<Ship {self.id} '{self.name}' {self.orbit}>"
        else:
            return f"<Ship {self.id} '{self.name}' {self.location}>"

    #################################################################################################
    def speed(self):
        """How fast the ship moves"""
        return 10

    #################################################################################################
    def set_destination(self, dest_system_id: SystemId) -> Optional[SystemId]:
        assert isinstance(dest_system_id, SystemId)
        if self.orbit:
            system = self.galaxy.systems[self.orbit]
            self.location = system.position
            if dest_system_id == system.id:
                self.destination = None
                return
        self.destination = dest_system_id
        return self.destination

    #################################################################################################
    def arrived_at_destination(self):
        dest = self.galaxy.systems[self.destination]
        self.orbit = dest
        self.location = dest.position
        self.destination = None

    #################################################################################################
    def move_towards_destination(self):
        dest = self.galaxy.systems[self.destination]
        if get_distance_tuple(self.location, dest.position) < self.speed() + 0.01:
            self.arrived_at_destination()

            return
        angle = math.atan2(dest.position[1] - self.location[1], dest.position[0] - self.location[0])
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
class ColonyBase(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 200
        self.space = 0
        self.command_points = 0
        self.maintenance = 0
        self.type = ShipType.ColonyBase

    def built(self) -> bool:
        """TODO: make the player choose"""
        for orbit in self.galaxy.systems[self.orbit]:
            if orbit and not orbit.owner and orbit.category == PlanetCategory.PLANET:
                orbit.colonize(self.owner)
                break
        return False


#####################################################################################################
class ColonyShip(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 25  # ?
        self.space = 0
        self.command_points = 1
        self.maintenance = 10
        self.coloniser = True
        self.type = ShipType.ColonyShip
        self.target_planet_id: Optional["PlanetId"] = None
        self.icon = "colony"

    #################################################################################################
    def arrived_at_destination(self):
        super().arrived_at_destination()
        if self.target_planet_id:
            planet = self.galaxy.planets[self.target_planet_id]
            planet.colonize(self.owner)

    #################################################################################################
    def set_destination_planet(self, dest_planet_id: PlanetId) -> None:
        self.set_destination(dest_planet_id)
        self.target_planet_id = dest_planet_id


#####################################################################################################
class Transport(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 25  # ?
        self.space = 0
        self.command_points = 1
        self.maintenance = 10
        self.type = ShipType.Transport
        self.icon = "transport"


#####################################################################################################
class Frigate(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 25
        self.space = 25
        self.type = ShipType.Frigate
        self.icon = f"frigate_{random.randint(0, 7)}"


#####################################################################################################
class Destroyer(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 85
        self.space = 60
        self.type = ShipType.Destroyer
        self.icon = f"destroyer_{random.randint(0, 7)}"


#####################################################################################################
class Cruiser(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 300
        self.space = 120
        self.type = ShipType.Cruiser
        self.icon = f"cruiser_{random.randint(0, 7)}"


#####################################################################################################
class Battleship(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 725
        self.space = 250
        self.type = ShipType.Battleship
        self.icon = f"battleship_{random.randint(0, 7)}"


#####################################################################################################
class Titan(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 1800
        self.space = 500
        self.type = ShipType.Titan
        self.icon = f"titan_{random.randint(0, 7)}"


#####################################################################################################
class DoomStar(Ship):
    def __init__(self, name: str, galaxy: "Galaxy"):
        super().__init__(name, galaxy)
        self.cost = 4800
        self.space = 1200
        self.type = ShipType.DoomStar
        self.icon = f"doomstar_{random.randint(0, 3)}"


#####################################################################################################
def select_ship_type_by_name(name: str, galaxy: "Galaxy") -> ShipId:
    ship_type = str_to_ship_type(name)
    ship = None
    match ship_type:
        case ShipType.ColonyBase:
            ship = ColonyBase("ColonyBase", galaxy)
        case ShipType.ColonyShip:
            ship = ColonyShip(f"Colony {counts[ShipType.ColonyShip]}", galaxy)
        case ShipType.Transport:
            counts[ShipType.Transport] += 1
            ship = Transport(f"Transport {counts[ShipType.Transport]}", galaxy)
        case ShipType.Frigate:
            counts[ShipType.Frigate] += 1
            ship = Frigate(f"Frigate {counts[ShipType.Frigate]}", galaxy)
        case ShipType.Destroyer:
            counts[ShipType.Destroyer] += 1
            ship = Destroyer(f"Destroyer {counts[ShipType.Destroyer]}", galaxy)
        case ShipType.Cruiser:
            counts[ShipType.Cruiser] += 1
            ship = Cruiser(f"Cruiser {counts[ShipType.Cruiser]}", galaxy)
        case ShipType.Battleship:
            counts[ShipType.Battleship] += 1
            ship = Battleship(f"Battleship {counts[ShipType.Battleship]}", galaxy)
        case ShipType.Titan:
            counts[ShipType.Titan] += 1
            ship = Titan(f"Titan {counts[ShipType.Titan]}", galaxy)
        case ShipType.DoomStar:
            counts[ShipType.DoomStar] += 1
            ship = DoomStar(f"DoomStar {counts[ShipType.DoomStar]}", galaxy)
    galaxy.ships[ship.id] = ship
    return ship.id


#####################################################################################################
def str_to_ship_type(type_str: str) -> ShipType:
    match type_str:
        case "ColonyBase":
            return ShipType.ColonyBase
        case "ColonyShip":
            return ShipType.ColonyShip
        case "Transport":
            return ShipType.Transport
        case "Frigate":
            return ShipType.Frigate
        case "Destroyer":
            return ShipType.Destroyer
        case "Cruiser":
            return ShipType.Cruiser
        case "Battleship":
            return ShipType.Battleship
        case "Titan":
            return ShipType.Titan
        case "DoomStar":
            return ShipType.DoomStar
        case _:
            raise NotImplementedError(f"Unhandled ship type {type_str=}")
