from typing import TYPE_CHECKING
from MooToo.constants import PopulationJobs, PlanetSize, PROD_RICHNESS_MAP, GRAVITY_MAP
from MooToo.utils import get_building

if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
def work_per(planet: "Planet") -> int:
    per = PROD_RICHNESS_MAP[planet.richness]
    for building in planet.buildings:
        per += get_building(building).prod_per_bonus(planet)
    return per


#####################################################################################################
def work_production(planet: "Planet") -> int:
    production = work_per(planet) * planet.jobs[PopulationJobs.WORKERS]
    production *= GRAVITY_MAP[planet.gravity]
    for building in planet.buildings:
        production += get_building(building).prod_bonus(planet)
    production = max(planet.jobs[PopulationJobs.WORKERS], production)

    return int(production)


#####################################################################################################
def work_cost(planet: "Planet") -> int:
    """AKA Pollution
    See https://strategywiki.org/wiki/Master_of_Orion_II:_Battle_at_Antares/Calculations
    """
    leader_coeff = 1  # Future stuff
    tolerance = 1  # Future stuff
    pp_base = work_production(planet)
    for building in planet.buildings:
        pp_base -= get_building(building).prod_bonus(planet)

    pollution_divisor = sum(get_building(building).pollution_divisor(planet) for building in planet.buildings) or 1
    planet_size = get_planet_size_coeff(planet.size)

    poll = pp_base / pollution_divisor * leader_coeff * tolerance - planet_size
    return max(0, int(poll // 2))


#####################################################################################################
def work_surplus(planet: "Planet") -> int:
    return work_production(planet) - work_cost(planet)


#####################################################################################################
def get_planet_size_coeff(size: PlanetSize) -> int:
    match size:
        case PlanetSize.TINY:
            return 2
        case PlanetSize.SMALL:
            return 4
        case PlanetSize.MEDIUM:
            return 6
        case PlanetSize.LARGE:
            return 8
        case PlanetSize.HUGE:
            return 10
