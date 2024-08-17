from typing import TYPE_CHECKING, Any, Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from ..server_utils import URL_PREFIX_SYSTEMS, get_galaxy
from ..serializers import system_reference_serializer
from ..serializers.system import system_serializer
from ...galaxy import Galaxy

if TYPE_CHECKING:
    from MooToo.system import System

router = APIRouter(prefix=URL_PREFIX_SYSTEMS)


#####################################################################################################
def get_safe_system(gal: Galaxy, system_id: int) -> "System":
    try:
        system = gal.systems[system_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return system


#####################################################################################################
@router.get("/")
async def system_list(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    systems = [system_reference_serializer(_) for _ in gal.systems.keys()]
    return {"status": "OK", "result": {"systems": systems}}


#####################################################################################################
@router.get("/{system_id:int}")
async def system_detail(system_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    system = get_safe_system(gal, system_id)
    return {
        "status": "OK",
        "result": {"system": system_serializer(system)},
    }


# EOF
