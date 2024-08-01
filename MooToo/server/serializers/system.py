from typing import Any, TYPE_CHECKING
from ..util import URL_PREFIX_PLANETS
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
    }
    for orbit in system.orbits:
        if not orbit:
            result["orbits"].append("")
        else:
            result["orbits"].append({"id": orbit.id, "url": f"{URL_PREFIX_PLANETS}/{orbit.id}"})
    return result
