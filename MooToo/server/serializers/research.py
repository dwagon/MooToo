from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo.research import Research


#####################################################################################################
def research_serializer(research: "Research") -> dict[str, Any]:
    return {"name": research.name, "cost": research.cost, "tag": research.tag}
