from typing import Any, TYPE_CHECKING
from . import system_reference_serializer, empire_id_serializer
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
        "owner": empire_id_serializer(ship.owner),
        "orbit": system_reference_serializer(ship.orbit) if ship.orbit else "",
        "destination": system_reference_serializer(ship.destination) if ship.destination else "",
    }
    return result
