from typing import Any, TYPE_CHECKING
from fastapi import APIRouter, status, HTTPException
from MooToo.planet_food import empire_food
from MooToo.server.server_utils import GALAXY
from ..server_utils import URL_PREFIX_EMPIRES
from ..serializers import empire_reference_serializer, ship_reference_serializer
from ..serializers.empire import empire_serializer

if TYPE_CHECKING:
    from MooToo.empire import Empire

router = APIRouter(prefix=URL_PREFIX_EMPIRES)


#####################################################################################################
def get_safe_empire(empire_id: int) -> "Empire":
    try:
        empire = GALAXY.empires[empire_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return empire


#####################################################################################################
@router.get("/")
async def list_empires() -> dict[str, Any]:
    data = [empire_reference_serializer(empire) for empire in GALAXY.empires.values() if empire]
    print(f"DBG {data=}")
    return {"status": "OK", "result": {"empires": data}}


#####################################################################################################
@router.get("/{empire_id:int}")
async def get_empire(empire_id: int) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"empire": empire_serializer(empire)}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/has_interest_in")
async def has_interest_in(empire_id: int, system_id: int) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"interest": empire.has_interest_in(system_id)}}


#####################################################################################################
@router.get("/{empire_id:int}/food")
async def get_food(empire_id) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    food = empire_food(empire)
    return {"status": "OK", "result": {"food": food}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/is_known")
def is_known_system(empire_id, system_id) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"known": empire.is_known_system(system_id)}}


#####################################################################################################
@router.get("/{empire_id:int}/researching")
def researching(empire_id) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"researching": empire.researching}}


#####################################################################################################
@router.get("/{empire_id:int}/ships")
def ships(empire_id) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"ships": [ship_reference_serializer(_) for _ in empire.ships]}}


# EOF
