from typing import TYPE_CHECKING
from MooToo.constants import PopulationJobs, GRAVITY_MAP
from MooToo.utils import get_building


if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
def science_production(planet: "Planet") -> int:
    production = planet.jobs[PopulationJobs.SCIENTISTS]
    production *= GRAVITY_MAP[planet.gravity]
    production = max(planet.jobs[PopulationJobs.SCIENTISTS], production)
    return int(production)


#####################################################################################################
def science_surplus(planet: "Planet") -> int:
    """To be consistent with other resources"""
    return science_production(planet)


#####################################################################################################
def science_per(planet: "Planet") -> int:
    per = 1
    for building in planet.buildings:
        per += get_building(building).research_per_bonus(planet)
    return per
