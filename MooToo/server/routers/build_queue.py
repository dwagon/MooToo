from typing import Any, Annotated
from fastapi import APIRouter, HTTPException, Depends
from ..server_utils import get_galaxy, URL_PREFIX_BUILD_QUEUE, get_safe_planet
from ..serializers.construct import construct_serializer
from ..serializers.build_queue import build_queue_serializer
from ...constants import Building
from ...construct import Construct, ConstructType

from ...galaxy import Galaxy


router = APIRouter(prefix=URL_PREFIX_BUILD_QUEUE)


#####################################################################################################
@router.get("/{planet_id:int}")
def build_queue(planet_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    return {"status": "OK", "result": {"build_queue": build_queue_serializer(planet.build_queue)}}


#####################################################################################################
@router.get("/{planet_id:int}/length")
def build_queue(planet_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    """Length of the build queue"""
    planet = get_safe_planet(planet_id, gal)
    return {"status": "OK", "result": {"length": len(planet.build_queue)}}


#####################################################################################################
@router.get("/{planet_id:int}/{index:int}")
def build_queue(planet_id: int, index: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    try:
        return {"status": "OK", "result": {"item": construct_serializer(planet.build_queue[index])}}
    except IndexError as exc:
        raise HTTPException(status_code=404, detail="Item not found") from exc


#####################################################################################################
@router.post("/{planet_id:int}/toggle/{construct_type:str}")
def build_queue_toggle(
    planet_id: int,
    construct_type: str,
    gal: Annotated[Galaxy, Depends(get_galaxy)],
    design_id: int = 0,
    building_tag: Building = None,
) -> dict[str, Any]:
    planet = get_safe_planet(planet_id, gal)
    match construct_type:
        case "spy":
            construct = Construct(ConstructType.SPY, gal)
        case "building":
            construct = Construct(ConstructType.BUILDING, gal, building_tag=building_tag)
        case "ship":
            construct = Construct(ConstructType.SHIP, gal, design_id=design_id)
        case "colony_base":
            construct = Construct(ConstructType.COLONY_BASE, gal)
        case "colony_ship":
            construct = Construct(ConstructType.COLONY_SHIP, gal)
        case "transport":
            construct = Construct(ConstructType.TRANSPORT, gal)
        case "freighter":
            construct = Construct(ConstructType.FREIGHTER, gal)
        case _:
            print(f"build_queue_toggle {construct_type=}")

    planet.build_queue.toggle(construct)
    return {"status": "OK", "result": {"build_queue": build_queue_serializer(planet.build_queue)}}


# EOF
