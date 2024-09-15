""" ship class """

import math

from typing import TYPE_CHECKING, Optional

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
        self.coloniser = False
        self.name = name
        self.destination: Optional[SystemId] = None
        self.location: tuple[int, int] = (-1, -1)
        self.orbit: Optional[SystemId] = None
        self.target_planet_id: Optional[PlanetId] = None

    #################################################################################################
    def __repr__(self):
        if self.orbit:
            return f"<Ship {self.id}: '{self.name}' {self.orbit} ({self.design_id=})>"
        else:
            return f"<Ship {self.id}: '{self.name}' {self.location} ({self.design_id=})>"

    #################################################################################################
    @property
    def icon(self):
        return self.galaxy.designs[self.design_id].icon

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
