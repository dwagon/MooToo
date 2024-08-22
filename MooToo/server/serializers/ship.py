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
        "coloniser": ship.coloniser,
        "target_planet_id": ship.target_planet_id,
        "speed": ship.speed(),
        "orbit": ship.orbit,
        "destination": ship.destination,
    }

    return result
