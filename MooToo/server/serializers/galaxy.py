from typing import Any, TYPE_CHECKING
from . import (
    empire_reference_serializer,
    system_reference_serializer,
    ship_reference_serializer,
    planet_reference_serializer,
)


if TYPE_CHECKING:
    from MooToo.galaxy import Galaxy


####################################################################################################
def galaxy_serializer(galaxy: "Galaxy") -> dict[str, Any]:
    return {
        "systems": [system_reference_serializer(_) for _ in galaxy.systems.values()],
        "empires": [empire_reference_serializer(_) for _ in galaxy.empires.values()],
        "planets": [planet_reference_serializer(_) for _ in galaxy.planets.values()],
        "ships": [ship_reference_serializer(_) for _ in galaxy.ships.values()],
        "turn_number": galaxy.turn_number,
    }
