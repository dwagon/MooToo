from typing import Any

from ..server_utils import (
    URL_PREFIX_SHIPS,
    URL_PREFIX_EMPIRES,
    URL_PREFIX_PLANETS,
    URL_PREFIX_SYSTEMS,
    URL_PREFIX_DESIGN,
)

from MooToo.utils import EmpireId, PlanetId, SystemId, ShipId, DesignId


#####################################################################################################
def empire_reference_serializer(empire_id: EmpireId) -> dict[str, Any]:
    assert isinstance(empire_id, EmpireId)
    return {"id": empire_id, "url": f"{URL_PREFIX_EMPIRES}/{empire_id}"}


#####################################################################################################
def planet_reference_serializer(planet_id: PlanetId) -> dict[str, Any]:
    assert isinstance(planet_id, PlanetId)
    return {"id": planet_id, "url": f"{URL_PREFIX_PLANETS}/{planet_id}"}


#####################################################################################################
def system_reference_serializer(system_id: SystemId) -> dict[str, Any]:
    assert isinstance(system_id, SystemId)
    return {"id": system_id, "url": f"{URL_PREFIX_SYSTEMS}/{system_id}"}


#####################################################################################################
def ship_reference_serializer(ship_id: ShipId):
    assert isinstance(ship_id, ShipId)
    return {"id": ship_id, "url": f"{URL_PREFIX_SHIPS}/{ship_id}"}


#####################################################################################################
def design_reference_serializer(design_id: DesignId):
    assert isinstance(design_id, DesignId)
    return {"id": design_id, "url": f"{URL_PREFIX_DESIGN}/{design_id}"}


# EOF
