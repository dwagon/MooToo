from typing import Any
from fastapi import APIRouter
from MooToo.utils import get_research
from MooToo.constants import Technology
from ..server_utils import URL_PREFIX_GALAXY, GALAXY
from ..serializers.galaxy import galaxy_serializer
from ..serializers.research import research_serializer

router = APIRouter(prefix=URL_PREFIX_GALAXY)


#####################################################################################################
@router.get("/")
def galaxy() -> dict[str, Any]:
    return {"status": "OK", "result": {"galaxy": galaxy_serializer(GALAXY)}}


#####################################################################################################
@router.post("/turn")
def turn() -> dict[str, Any]:
    return {"status": "OK", "result": {"turn_number": GALAXY.turn()}}


#####################################################################################################
@router.get("/research/{tech}")
def research(tech: Technology) -> dict[str, Any]:
    return {"status": "OK", "result": {"research": research_serializer(get_research(tech))}}


# EOF
