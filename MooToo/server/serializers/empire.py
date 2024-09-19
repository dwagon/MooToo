from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from MooToo.empire import Empire


#####################################################################################################
def empire_serializer(empire: "Empire") -> dict[str, Any]:

    return {
        "id": empire.id,
        "name": empire.name,
        "colour": empire.colour,
        "government": empire.government,
        "money": empire.money,
        "income": empire.income,
        "known_systems": empire.known_systems,
        "owned_planets": empire.owned_planets,
        "researching": empire.researching,
        "research_spent": empire.research_spent,
        "research_points": empire.get_research_points(),
        "freighters": empire.freighters,
        "freighters_used": empire.freighters_used(),
        "known_techs": empire.known_techs,
    }
