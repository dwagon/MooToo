from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo.ship import Ship


#####################################################################################################
def ship_serializer(ship: "Ship") -> Any:
    result: dict[str, Any] = {
        "id": ship.id,
        "name": ship.name,
        "icon": ship.icon,
        "owner": ship.owner,
        "design_id": ship.design_id,
        "location_id": ship.location,
        "owner_id": ship.owner,
        "target_planet_id": ship.target_planet_id,
        "speed": ship.speed(),
        "orbit": ship.orbit,
        "destination": ship.destination,
        "range": ship.range,
    }

    return result
