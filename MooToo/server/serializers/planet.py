from typing import TYPE_CHECKING, Any
from ..serializers import empire_reference_serializer

if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
def planet_serializer(planet: "Planet") -> dict[str, Any]:
    return {
        "status": "OK",
        "result": {
            "planet": {
                "id": planet.id,
                "name": planet.name,
                "category": planet.category,
                "owner": empire_reference_serializer(planet.owner),
                "size": planet.size,
                "richness": planet.richness,
                "climate": planet.climate,
                "gravity": planet.gravity,
                "arc": planet.arc,
                "climate_image": planet.climate_image,
                "morale": planet.morale(),
                "max_pop": planet.max_population(),
                "population": planet.current_population(),
            },
        },
    }
