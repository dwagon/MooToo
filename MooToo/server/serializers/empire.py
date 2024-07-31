from typing import Any, TYPE_CHECKING
from . import system_reference_serializer, planet_reference_serializer

if TYPE_CHECKING:
    from MooToo.empire import Empire


#####################################################################################################
def empire_serializer(empire: "Empire") -> dict[str, Any]:
    known_systems = [system_reference_serializer(_) for _ in empire.known_systems]
    owned_planets = [planet_reference_serializer(_) for _ in empire.owned_planets]

    return {
        "id": empire.id,
        "name": empire.name,
        "colour": empire.colour,
        "government": empire.government,
        "money": empire.money,
        "income": empire.income,
        "known_systems": known_systems,
        "owned_planets": owned_planets,
        "researching": empire.researching,
        "research_spent": empire.research_spent,
        "research_points": empire.get_research_points(),
        "freighters": empire.freighters,
        "freighters_used": empire.freighters_used(),
        "known_techs": empire.known_techs,
    }
