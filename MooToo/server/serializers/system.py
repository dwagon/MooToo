from typing import Any, TYPE_CHECKING
from .location import location_serializer

if TYPE_CHECKING:
    from MooToo.system import System


#####################################################################################################
def system_serializer(system: "System") -> dict[str, Any]:
    result = {
        "id": system.id,
        "position": location_serializer(system.position),
        "name": system.name,
        "colour": system.colour.name,
        "orbits": [],
        "planets": system.planets,
    }
    for orbit in system.orbits:
        if not orbit:
            result["orbits"].append("")
        else:
            result["orbits"].append(orbit)
    return result
