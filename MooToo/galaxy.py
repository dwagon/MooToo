""" Galaxy class"""

import io
import jsonpickle
from typing import TYPE_CHECKING, Optional
from MooToo.utils import SystemId, PlanetId, ShipId, EmpireId, unique_ship_id, ConstructId, DesignId, unique_design_id

if TYPE_CHECKING:
    from MooToo.system import System
    from MooToo.empire import Empire
    from MooToo.planet import Planet
    from MooToo.ship import Ship
    from MooToo.construct import Construct
    from MooToo.ship_design import ShipDesign


#####################################################################################################
class Galaxy:
    def __init__(self):
        self.systems: dict[SystemId, "System"] = {}
        self.empires: dict[EmpireId, Optional["Empire"]] = {}
        self.planets: dict[PlanetId, "Planet"] = {}
        self.ships: dict[ShipId, "Ship"] = {}
        self.constructs: dict[ConstructId, "Construct"] = {}
        self.designs: dict[DesignId, "ShipDesign"] = {}
        self.turn_number = 0
        self.ship_id_generator = unique_ship_id()
        self.design_id_generator = unique_design_id()

    #####################################################################################################
    def turn(self) -> int:
        """End of turn"""
        self.turn_number += 1
        for system in self.systems.values():
            system.turn()
        for empire in self.empires.values():
            empire.turn()
        return self.turn_number

    #####################################################################################################
    def add_design(self, design: "ShipDesign") -> DesignId:
        design_id = next(self.design_id_generator)
        self.designs[design_id] = design
        return design_id


#####################################################################################################
def save(galaxy: Galaxy, filename: str) -> None:
    file_name = f"{filename}_{galaxy.turn_number % 10}.json"
    with open(file_name, "w") as out_handle:
        out_handle.write(jsonpickle.encode(galaxy, keys=True, indent=2, warn=True))


#####################################################################################################
def load(file_handle: io.TextIOWrapper) -> Galaxy:
    return jsonpickle.loads(file_handle.read(), keys=True)


# EOF
