""" system class"""

from typing import TYPE_CHECKING, Optional
from MooToo.utils import SystemId, PlanetId, ShipId
from MooToo.constants import StarColour

if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


#####################################################################################################
class System:
    def __init__(self, system_id: SystemId, name: str, colour: StarColour, position: tuple[int, int], galaxy: "Galaxy"):
        self.id = system_id
        self.position = position
        self.name = name
        self.colour = colour
        self.orbits: list[Optional[PlanetId]] = []
        self.galaxy = galaxy
        self._index = 0

    #####################################################################################################
    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        try:
            data = self.orbits[self._index]
        except IndexError as e:
            raise StopIteration from e
        self._index += 1
        return data

    #####################################################################################################
    def __repr__(self):
        return f"<System {self.position}>"

    #####################################################################################################
    def unoccupied_planet(self) -> bool:
        """Return True if there is an unoccupied planet in the system"""
        for planet_id in self:
            planet = self.galaxy.planets[planet_id]
            if planet and not planet.owner:
                return True
        return False

    #####################################################################################################
    def turn(self):
        for planet_id in self:
            if planet := self.galaxy.planets[planet_id]:
                planet.turn()

    #####################################################################################################
    def ships_in_orbit(self) -> list[ShipId]:
        """Return the list of ships (of all players) in orbit"""
        ships: list[ShipId] = []
        for emp in self.galaxy.empires.values():
            ships.extend(ship_id for ship_id in emp.ships if self.galaxy.ships[ship_id].location == self.id)
        return ships


# EOF
