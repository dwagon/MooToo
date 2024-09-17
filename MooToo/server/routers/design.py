from typing import Any, Annotated
from fastapi import status, HTTPException
from fastapi import APIRouter, Depends
from ..server_utils import get_galaxy, URL_PREFIX_DESIGN
from ..serializers.ship_design import ship_design_serializer
from ..serializers import design_reference_serializer
from ...galaxy import Galaxy
from ...ship_design import ShipDesign

router = APIRouter(prefix=URL_PREFIX_DESIGN)


#####################################################################################################
def get_safe_design(design_id: int, gal: Galaxy) -> "ShipDesign":
    try:
        design = gal.designs[design_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return design


#####################################################################################################
@router.get("/")
def planet_list(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    data = [design_reference_serializer(_) for _ in gal.designs.keys()]
    return {"status": "OK", "result": {"designs": data}}


#####################################################################################################
@router.get("/{design_id:int}")
async def design_detail(design_id: int, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    design = get_safe_design(design_id, gal)
    return {"status": "OK", "result": {"design": ship_design_serializer(design)}}


# EOF
