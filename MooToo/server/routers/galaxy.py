from typing import Any
from fastapi import APIRouter
from MooToo.utils import get_distance
from ..server_utils import URL_PREFIX_GALAXY, GALAXY
from ..serializers.galaxy import galaxy_serializer

router = APIRouter(prefix=URL_PREFIX_GALAXY)


#####################################################################################################
@router.get("/")
def galaxy() -> dict[str, Any]:
    return {"status": "OK", "result": {"galaxy": galaxy_serializer(GALAXY)}}


#####################################################################################################
@router.get("/get_distance")
def get_distance(x1, y1, x2, y2) -> dict[str, Any]:
    return {"status": "OK", "result": {"distance": get_distance(x1, y1, x2, y2)}}


#####################################################################################################
@router.post("/turn")
def turn() -> dict[str, Any]:
    return {"status": "OK", "result": {"turn_number": GALAXY.turn()}}


# EOF
