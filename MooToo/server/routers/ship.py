from typing import TYPE_CHECKING, Any
from fastapi import APIRouter, HTTPException, status
from MooToo.server.server_utils import GALAXY
from MooToo.utils import SystemId
from ..server_utils import URL_PREFIX_SHIPS
from ..serializers import ship_reference_serializer
from ..serializers.ship import ship_serializer

if TYPE_CHECKING:
    from MooToo.ship import Ship

router = APIRouter(prefix=URL_PREFIX_SHIPS)


#####################################################################################################
def get_safe_ship(ship_id: int) -> "Ship":
    try:
        ship = GALAXY.ships[ship_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return ship


#####################################################################################################
@router.get("/")
def ship_list() -> dict[str, Any]:
    data = [ship_reference_serializer(_) for _ in GALAXY.ships.keys()]
    return {"status": "OK", "result": {"ships": data}}


#####################################################################################################
@router.get("/{ship_id:int}")
async def ship_detail(ship_id: int) -> dict[str, Any]:
    ship = get_safe_ship(ship_id)

    return {
        "status": "OK",
        "result": {"ship": ship_serializer(ship)},
    }


#####################################################################################################
@router.post("/{ship_id:int}/set_destination")
def set_destination(ship_id: int, destination_id: SystemId) -> dict[str, Any]:
    ship = get_safe_ship(ship_id)
    ship.set_destination(destination_id)

    return {
        "status": "OK",
        "result": {"ship": ship_serializer(ship)},
    }


# EOF
