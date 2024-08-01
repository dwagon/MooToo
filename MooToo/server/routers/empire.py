from typing import Any, TYPE_CHECKING
from fastapi import APIRouter, status, HTTPException
from MooToo.server.util import GALAXY
from ..util import URL_PREFIX_EMPIRES
from ..serializers import empire_reference_serializer
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
def list_empires() -> dict[str, Any]:
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
def has_interest_in(empire_id: int, system_id: int) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"interest": empire.has_interest_in(system_id)}}
