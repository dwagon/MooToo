from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from MooToo.construct import Construct


def construct_serializer(construct: "Construct") -> dict[str, Any]:
    return {"category": construct.category, "design_id": construct.design_id, "building_tag": construct.building_tag}
