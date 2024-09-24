""" ship class """

import math

from typing import TYPE_CHECKING, Optional

from MooToo.constants import Technology
from MooToo.ship_design import ShipDesign, HullType
from MooToo.utils import get_distance_tuple, ShipId, EmpireId, SystemId, PlanetId, DesignId


if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
class Ship:
    """Things that move - instances of ship designs"""

    def __init__(self, name: str, design_id: DesignId, galaxy: "Galaxy"):
        self.design_id = design_id
        self.galaxy = galaxy
        self.id: ShipId = next(galaxy.ship_id_generator)
        self.owner: EmpireId = 0
        self.command_points = 0
        self.maintenance = 0
        self.name = name
        self.destination: Optional[SystemId] = None  # Where system we are going to
        self.location: tuple[int, int] = (-1, -1)  # What coords we are at
        self.orbit: Optional[SystemId] = None  # What system we are at
        self.target_planet_id: Optional[PlanetId] = None  # Which planet coloniser is aimed at

    #################################################################################################
    @property
    def design(self) -> ShipDesign:
        return self.galaxy.designs[self.design_id]

    #################################################################################################
    @property
    def coloniser(self) -> bool:
        return self.design.hull == HullType.ColonyShip

    #################################################################################################
    def __repr__(self):
        if self.orbit:
            return f"<Ship {self.id}: '{self.name}' {self.orbit} ({self.design_id=})>"
        else:
            return f"<Ship {self.id}: '{self.name}' {self.location} ({self.design_id=})>"

    #################################################################################################
    @property
    def icon(self):
        return self.design.icon

    #################################################################################################
    def speed(self):
        """How fast the ship moves"""
        return 10

    #################################################################################################
    @property
    def range(self) -> int:
        """How far the ship moves"""
        # TODO - extended fuel tanks
        _range = 0
        known_techs = self.galaxy.empires[self.owner].known_techs
        if Technology.THORIUM_FUEL_CELLS in known_techs:
            _range = 9999
        elif Technology.URIDIUM_FUEL_CELLS in known_techs:
            _range = 12
        elif Technology.IRIDIUM_FUEL_CELLS in known_techs:
            _range = 9
        elif Technology.DEUTERIUM_FUEL_CELLS in known_techs:
            _range = 6
        else:
            _range = 4  # Standard
        # Ships that are one way
        if self.design.hull in (HullType.ColonyShip, HullType.OutpostShip):
            _range *= 2
        return _range

    #################################################################################################
    def set_destination(self, dest_system_id: SystemId) -> Optional[SystemId]:
        assert isinstance(dest_system_id, SystemId)
        if self.orbit:
            system = self.galaxy.systems[self.orbit]
            self.location = system.position
            if dest_system_id == system.id:
                self.destination = None
                return
        if get_distance_tuple(self.location, self.galaxy.systems[dest_system_id].position) > self.range:
            return
        self.destination = dest_system_id
        return self.destination

    #################################################################################################
    def set_destination_planet(self, dest_planet_id: PlanetId) -> None:
        assert isinstance(dest_planet_id, PlanetId)
        dest_system_id = self.galaxy.planets[dest_planet_id].system_id
        self.set_destination(dest_system_id)
        self.target_planet_id = dest_planet_id

    #################################################################################################
    def arrived_at_destination(self):
        assert isinstance(self.destination, SystemId)
        dest = self.galaxy.systems[self.destination]
        self.orbit = self.destination
        self.location = dest.position
        self.destination = None
        if self.coloniser and self.target_planet_id:
            self.galaxy.empires[self.owner].colonize(self.target_planet_id, self.id)

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


# EOF
