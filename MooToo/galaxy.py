""" Galaxy class"""

import io
import jsonpickle
from typing import TYPE_CHECKING, Optional
from MooToo.utils import (
    SystemId,
    PlanetId,
    ShipId,
    EmpireId,
    unique_ship_id,
)

if TYPE_CHECKING:
    from MooToo.system import System
    from MooToo.empire import Empire
    from MooToo.planet import Planet
    from MooToo.ship import Ship


#####################################################################################################
class Galaxy:
    def __init__(self):
        self.systems: dict[SystemId, "System"] = {}
        self.empires: dict[EmpireId, Optional["Empire"]] = {}
        self.planets: dict[PlanetId, "Planet"] = {}
        self.ships: dict[ShipId, "Ship"] = {}
        self.turn_number = 0
        self.planet_num = 0
        self.ship_id_generator = unique_ship_id()

    #####################################################################################################
    def turn(self):
        """End of turn"""
        self.turn_number += 1
        for system in self.systems.values():
            system.turn()
        for empire in self.empires.values():
            empire.turn()


#####################################################################################################
def save(galaxy: Galaxy, filename: str) -> None:
    file_name = f"{filename}_{galaxy.turn_number % 10}.json"
    with open(file_name, "w") as out_handle:
        out_handle.write(jsonpickle.encode(galaxy, keys=True, indent=2, warn=True))


#####################################################################################################
def load(file_handle: io.TextIOWrapper) -> Galaxy:
    return jsonpickle.loads(file_handle.read(), keys=True)


# EOF
