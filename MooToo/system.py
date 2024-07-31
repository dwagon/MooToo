""" system class"""

from typing import TYPE_CHECKING
from MooToo.planet import Planet
from MooToo.utils import SystemId
from MooToo.constants import StarColour

if TYPE_CHECKING:
    from MooToo.ship import Ship
    from MooToo.galaxy import Galaxy


#####################################################################################################
class System:
    def __init__(self, system_id: SystemId, name: str, colour: StarColour, position: tuple[int, int], galaxy: "Galaxy"):
        self.id = system_id
        self.position = position
        self.name = name
        self.colour = colour
        self.orbits: list[Planet | None] = []
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
        for planet in self:
            if planet and not planet.owner:
                return True
        return False

    #####################################################################################################
    def turn(self):
        for planet in self:
            if planet:
                planet.turn()

    #####################################################################################################
    def ships_in_orbit(self) -> list["Ship"]:
        """Return the list of ships (of all players) in orbit"""
        ships: list["Ship"] = []
        for emp in self.galaxy.empires.values():
            ships.extend([_ for _ in emp.ships if _.location == self])
        return ships


# EOF
