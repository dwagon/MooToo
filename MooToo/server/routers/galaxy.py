from typing import Any, Annotated
from fastapi import APIRouter, Depends
from MooToo.utils import get_research
from MooToo.constants import Technology
from ..server_utils import URL_PREFIX_GALAXY, get_galaxy
from ..serializers.galaxy import galaxy_serializer
from ..serializers.research import research_serializer
from ...galaxy import Galaxy

router = APIRouter(prefix=URL_PREFIX_GALAXY)


#####################################################################################################
@router.get("/")
def galaxy(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    return {"status": "OK", "result": {"galaxy": galaxy_serializer(gal)}}


#####################################################################################################
@router.post("/turn")
def turn(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    return {"status": "OK", "result": {"turn_number": gal.turn()}}


#####################################################################################################
@router.get("/research/{tech}")
def research(tech: Technology) -> dict[str, Any]:
    return {"status": "OK", "result": {"research": research_serializer(get_research(tech))}}


# EOF
