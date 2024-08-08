from typing import Any, TYPE_CHECKING
from . import empire_reference_serializer, system_reference_serializer
from .location import location_serializer

if TYPE_CHECKING:
    from MooToo.ship import Ship


#####################################################################################################
def ship_serializer(ship: "Ship") -> Any:
    result: dict[str, Any] = {
        "id": ship.id,
        "name": ship.name,
        "icon": ship.icon,
        "location": location_serializer(ship.location),
        "type": ship.type.name,
        "owner": empire_reference_serializer(ship.owner),
        "destination": ship.destination,
    }
    result["orbit"] = system_reference_serializer(ship.orbit) if ship.orbit is not None else None
    return result
