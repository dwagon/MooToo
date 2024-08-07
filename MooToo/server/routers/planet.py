from typing import Any, TYPE_CHECKING
from fastapi import APIRouter, status, HTTPException
from ..util import GALAXY, URL_PREFIX_PLANETS
from MooToo.ship import str_to_ship_type
from ..serializers.planet import planet_serializer
from ..serializers import planet_reference_serializer

if TYPE_CHECKING:
    from MooToo.planet import Planet

router = APIRouter(prefix=URL_PREFIX_PLANETS)


#####################################################################################################
def get_safe_planet(planet_id: int) -> "Planet":
    try:
        planet = GALAXY.planets[planet_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return planet


#####################################################################################################
@router.get("/")
def planet_list() -> dict[str, Any]:
    data = [planet_reference_serializer(_) for _ in GALAXY.planets.values()]
    return {"status": "OK", "result": {"planets": data}}


#####################################################################################################
@router.get("/{planet_id:int}")
async def planet_detail(planet_id: int) -> dict[str, Any]:
    planet = get_safe_planet(planet_id)
    return planet_serializer(planet)


#####################################################################################################
@router.get("/planet_id:int}/can_build_ship/{ship_type}")
def planet_can_build_ship(planet_id: int, ship_type: str) -> dict[str, Any]:
    planet = get_safe_planet(planet_id)
    try:
        real_ship_type = str_to_ship_type(ship_type)
    except NotImplementedError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e

    can_build = planet.can_build_ship(real_ship_type)
    return {"status": "OK", "result": {"ship_type": real_ship_type.name, "can_build": can_build}}
