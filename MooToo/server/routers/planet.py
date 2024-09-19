from typing import Any, TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends
from ..server_utils import get_galaxy, URL_PREFIX_PLANETS, get_safe_planet
from ..serializers.planet import planet_serializer
from ..serializers import planet_reference_serializer
from ...constants import PopulationJobs
from ...galaxy import Galaxy
from ...ship_design import HullType


router = APIRouter(prefix=URL_PREFIX_PLANETS)


#####################################################################################################
@router.get("/")
def planet_list(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    data = [planet_reference_serializer(_) for _ in gal.planets.keys()]
    return {"status": "OK", "result": {"planets": data}}


#####################################################################################################
@router.get("/{planet_id:int}")
async def planet_detail(planet_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    return {"status": "OK", "result": {"planet": planet_serializer(planet)}}


#####################################################################################################
@router.get("/{planet_id:int}/can_build_ship/{ship_type}")
def planet_can_build_ship(
    planet_id: int, ship_type: str, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    real_ship_type = HullType(ship_type)
    can_build = planet.can_build_ship(real_ship_type)
    return {"status": "OK", "result": {"ship_type": real_ship_type.name, "can_build": can_build}}


#####################################################################################################
@router.post("/{planet_id:int}/move_workers")
def planet_move_workers(
    planet_id: int,
    num: int,
    src_job: PopulationJobs,
    target_job: PopulationJobs,
    gal: Annotated[Galaxy, Depends(get_galaxy)],
) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    planet.move_workers(num, src_job, target_job)
    return {"status": "OK", "result": {"planet": planet_serializer(planet)}}


#####################################################################################################
@router.get("/{planet_id:int}/available_to_build")
def available_to_build(planet_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    return {"status": "OK", "result": {"available": planet.available_to_build()}}


# EOF
