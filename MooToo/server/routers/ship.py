from typing import TYPE_CHECKING, Any, Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from MooToo.server.server_utils import get_galaxy
from MooToo.utils import SystemId
from ..server_utils import URL_PREFIX_SHIPS
from ..serializers import ship_reference_serializer
from ..serializers.ship import ship_serializer
from ...galaxy import Galaxy

if TYPE_CHECKING:
    from MooToo.ship import Ship

router = APIRouter(prefix=URL_PREFIX_SHIPS)


#####################################################################################################
def get_safe_ship(ship_id: int, gal: Galaxy) -> "Ship":
    try:
        ship = gal.ships[ship_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return ship


#####################################################################################################
@router.get("/")
def ship_list(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    data = [ship_reference_serializer(_) for _ in gal.ships.keys()]
    return {"status": "OK", "result": {"ships": data}}


#####################################################################################################
@router.get("/{ship_id:int}")
async def ship_detail(ship_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    ship = get_safe_ship(ship_id, gal)

    return {
        "status": "OK",
        "result": {"ship": ship_serializer(ship)},
    }


#####################################################################################################
@router.post("/{ship_id:int}/set_destination")
def set_destination(
    ship_id: int, destination_id: SystemId, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    ship = get_safe_ship(ship_id, gal)
    ship.set_destination(destination_id)

    return {
        "status": "OK",
        "result": {"ship": ship_serializer(ship)},
    }


# EOF
