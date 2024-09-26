from typing import Any, TYPE_CHECKING, Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from MooToo.planet_food import empire_food
from MooToo.server.server_utils import get_galaxy
from ..server_utils import URL_PREFIX_EMPIRES
from ..serializers import empire_reference_serializer, ship_reference_serializer
from ..serializers.empire import empire_serializer
from ...galaxy import Galaxy
from ...utils import EmpireId, SystemId, PlanetId, ShipId
from MooToo.constants import Technology, PopulationJobs

if TYPE_CHECKING:
    from MooToo.empire import Empire

router = APIRouter(prefix=URL_PREFIX_EMPIRES)


#####################################################################################################
def get_safe_empire(empire_id: EmpireId, gal: Galaxy) -> "Empire":
    try:
        empire = gal.empires[empire_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return empire


#####################################################################################################
@router.get("/")
async def list_empires(gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    data = [empire_reference_serializer(_) for _ in gal.empires.keys() if _]
    return {"status": "OK", "result": {"empires": data}}


#####################################################################################################
@router.get("/{empire_id:int}")
async def get_empire(empire_id: EmpireId, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"empire": empire_serializer(empire)}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/has_interest_in")
async def has_interest_in(
    empire_id: EmpireId, system_id: SystemId, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    interest = empire.has_interest_in(system_id)
    return {"status": "OK", "result": {"interest": interest}}


#####################################################################################################
@router.get("/{empire_id:int}/known_systems")
async def known_systems(empire_id: EmpireId, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"known": empire.known_systems}}


#####################################################################################################
@router.get("/{empire_id:int}/food")
async def get_food(empire_id: EmpireId, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    food = empire_food(empire)
    return {"status": "OK", "result": {"food": food}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/is_known")
def is_known_system(
    empire_id: EmpireId, system_id: SystemId, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"known": empire.is_known_system(system_id)}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/has_interest_in")
def has_interest_in(
    empire_id: EmpireId, system_id: SystemId, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"interest": empire.has_interest_in(system_id)}}


#####################################################################################################
@router.get("/{empire_id:int}/researching")
def researching(empire_id: EmpireId, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"researching": empire.researching}}


#####################################################################################################
@router.get("/{empire_id:int}/ships")
def ships(empire_id: EmpireId, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"ships": [ship_reference_serializer(_) for _ in empire.ships]}}


#####################################################################################################
@router.get("/{empire_id:int}/{category:str}/next_research")
def next_research(empire_id: EmpireId, category, gal: Annotated[Galaxy, Depends(get_galaxy)]) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    return {"status": "OK", "result": {"research": empire.next_research(category)}}


#####################################################################################################
@router.post("/{empire_id:int}/start_researching")
def start_research(
    empire_id: EmpireId, tech: Technology, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    empire.start_researching(tech)

    return {
        "status": "OK",
        "result": {"research": empire_serializer(empire)},
    }


#####################################################################################################
@router.post("/{empire_id:int}/send_coloniser")
def send_colony(
    empire_id: EmpireId, dest_planet_id: PlanetId, gal: Annotated[Galaxy, Depends(get_galaxy)]
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    ship_id = empire.send_coloniser(dest_planet_id)

    return {
        "status": "OK",
        "result": {"ship": ship_id},
    }


#####################################################################################################
@router.get("/{empire_id:int}/in_range")
def in_range(
    empire_id: EmpireId, destination_id: SystemId, ship_id: ShipId, gal: Annotated[Galaxy, Depends(get_galaxy)]
):
    empire = get_safe_empire(empire_id, gal)
    ans = empire.in_range(destination_id, ship_id)
    return {"status": "OK", "result": {"in_range": ans}}


#####################################################################################################
@router.post("/{empire_id:int}/migrate")
def migrate(
    empire_id: EmpireId,
    num: int,
    src_planet_id: PlanetId,
    src_job: PopulationJobs,
    dest_planet_id: PlanetId,
    dst_job: PopulationJobs,
    gal: Annotated[Galaxy, Depends(get_galaxy)],
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id, gal)
    empire.migrate(num, src_planet_id, src_job, dest_planet_id, dst_job)

    return {
        "status": "OK",
        "result": {"empire": empire_serializer(empire)},
    }


# EOF
