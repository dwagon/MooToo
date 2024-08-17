from typing import Any, TYPE_CHECKING
from fastapi import APIRouter, status, HTTPException
from MooToo.planet_food import empire_food
from MooToo.server.server_utils import GALAXY
from ..server_utils import URL_PREFIX_EMPIRES
from ..serializers import empire_reference_serializer, ship_reference_serializer
from ..serializers.empire import empire_serializer
from ...utils import EmpireId, SystemId, PlanetId
from MooToo.constants import Technology, PopulationJobs

if TYPE_CHECKING:
    from MooToo.empire import Empire

router = APIRouter(prefix=URL_PREFIX_EMPIRES)


#####################################################################################################
def get_safe_empire(empire_id: EmpireId) -> "Empire":
    try:
        empire = GALAXY.empires[empire_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return empire


#####################################################################################################
@router.get("/")
async def list_empires() -> dict[str, Any]:
    data = [empire_reference_serializer(empire) for empire in GALAXY.empires.values() if empire]
    return {"status": "OK", "result": {"empires": data}}


#####################################################################################################
@router.get("/{empire_id:int}")
async def get_empire(empire_id: EmpireId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"empire": empire_serializer(empire)}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/has_interest_in")
async def has_interest_in(empire_id: EmpireId, system_id: SystemId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    interest = empire.has_interest_in(system_id)
    return {"status": "OK", "result": {"interest": interest}}


#####################################################################################################
@router.get("/{empire_id:int}/known_systems")
async def known_systems(empire_id: EmpireId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"known": empire.known_systems}}


#####################################################################################################
@router.get("/{empire_id:int}/food")
async def get_food(empire_id: EmpireId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    food = empire_food(empire)
    return {"status": "OK", "result": {"food": food}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/is_known")
def is_known_system(empire_id: EmpireId, system_id: SystemId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"known": empire.is_known_system(system_id)}}


#####################################################################################################
@router.get("/{empire_id:int}/{system_id:int}/has_interest_in")
def has_interest_in(empire_id: EmpireId, system_id: SystemId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"interest": empire.has_interest_in(system_id)}}


#####################################################################################################
@router.get("/{empire_id:int}/researching")
def researching(empire_id: EmpireId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"researching": empire.researching}}


#####################################################################################################
@router.get("/{empire_id:int}/ships")
def ships(empire_id: EmpireId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"ships": [ship_reference_serializer(_) for _ in empire.ships]}}


#####################################################################################################
@router.get("/{empire_id:int}/{category:str}/next_research")
def next_research(empire_id: EmpireId, category) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    return {"status": "OK", "result": {"research": empire.next_research(category)}}


#####################################################################################################
@router.post("/{empire_id:int}/start_researching")
def start_research(empire_id: EmpireId, tech: Technology) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    empire.start_researching(tech)

    return {
        "status": "OK",
        "result": {"research": empire_serializer(empire)},
    }


#####################################################################################################
@router.post("/{empire_id:int}/send_coloniser")
def send_colony(empire_id: EmpireId, dest_planet_id: PlanetId) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    empire.send_coloniser(dest_planet_id)

    return {
        "status": "OK",
        "result": {"empire": empire_serializer(empire)},
    }


#####################################################################################################
@router.post("/{empire_id:int}/migrate")
def migrate(
    empire_id: EmpireId,
    num: int,
    src_planet_id: PlanetId,
    src_job: PopulationJobs,
    dest_planet_id: PlanetId,
    dst_job: PopulationJobs,
) -> dict[str, Any]:
    empire = get_safe_empire(empire_id)
    empire.migrate(num, src_planet_id, src_job, dest_planet_id, dst_job)

    return {
        "status": "OK",
        "result": {"empire": empire_serializer(empire)},
    }


# EOF
