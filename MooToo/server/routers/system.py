from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, HTTPException, status
from MooToo.server.util import GALAXY
from ..util import URL_PREFIX_SYSTEMS
from ..serializers import system_reference_serializer
from ..serializers.system import system_serializer

if TYPE_CHECKING:
    from MooToo.system import System

router = APIRouter(prefix=URL_PREFIX_SYSTEMS)


#####################################################################################################
def get_safe_system(system_id: int) -> "System":
    try:
        system = GALAXY.systems[system_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return system


#####################################################################################################
@router.get("/")
async def system_list() -> dict[str, Any]:
    systems = [system_reference_serializer(_) for _ in GALAXY.systems.values()]
    return {"status": "OK", "result": {"systems": systems}}


#####################################################################################################
@router.get("/{system_id:int}")
async def system_detail(system_id: int) -> dict[str, Any]:
    system = get_safe_system(system_id)
    return {
        "status": "OK",
        "result": {"system": system_serializer(system)},
    }


# EOF
