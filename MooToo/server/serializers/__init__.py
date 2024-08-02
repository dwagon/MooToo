from typing import Any, TYPE_CHECKING

from ..server_utils import URL_PREFIX_SHIPS, URL_PREFIX_EMPIRES, URL_PREFIX_PLANETS, URL_PREFIX_SYSTEMS

if TYPE_CHECKING:
    from MooToo.empire import Empire
    from MooToo.planet import Planet
    from MooToo.system import System
    from MooToo.ship import Ship


#####################################################################################################
def empire_reference_serializer(empire: "Empire") -> dict[str, Any]:
    return {"id": empire.id, "url": f"{URL_PREFIX_EMPIRES}/{empire.id}"}


#####################################################################################################
def empire_id_serializer(empire_id: int) -> dict[str, Any]:
    return {"id": empire_id, "url": f"{URL_PREFIX_EMPIRES}/{empire_id}"}


#####################################################################################################
def planet_reference_serializer(planet: "Planet") -> dict[str, Any]:
    return {"id": planet.id, "url": f"{URL_PREFIX_PLANETS}/{planet.id}"}


#####################################################################################################
def system_reference_serializer(system: "System") -> dict[str, Any]:
    return {"id": system.id, "url": f"{URL_PREFIX_SYSTEMS}/{system.id}"}


#####################################################################################################
def ship_reference_serializer(ship: "Ship"):
    return {"id": ship.id, "url": f"{URL_PREFIX_SHIPS}/{ship.id}"}
