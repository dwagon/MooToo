from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo.ship_design import ShipDesign


#####################################################################################################
def ship_design_serializer(design: "ShipDesign") -> Any:
    result: dict[str, Any] = {"id": design.id, "name": design.name, "hull": design.hull}

    return result
