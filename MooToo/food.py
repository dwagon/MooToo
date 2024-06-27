""" Food related functions"""

from typing import TYPE_CHECKING
from MooToo.constants import PopulationJobs, FOOD_CLIMATE_MAP, GRAVITY_MAP
from MooToo.utils import get_building

if TYPE_CHECKING:
    from MooToo.planet import Planet
    from MooToo.empire import Empire


#####################################################################################################
def food_surplus(planet: "Planet") -> int:
    """How much food surplus (or hunger) do we have"""
    return food_production(planet) - food_cost(planet)


#####################################################################################################
def food_per(planet: "Planet") -> int:
    """How much food each farmer produces"""
    per = FOOD_CLIMATE_MAP[planet.climate]
    for building in planet.buildings:
        per += get_building(building).food_per_bonus(planet)
    return per


#####################################################################################################
def food_production(planet: "Planet") -> int:
    production = food_per(planet) * planet.jobs[PopulationJobs.FARMERS]
    production *= GRAVITY_MAP[planet.gravity]
    for building in planet.buildings:
        production += get_building(building).food_bonus(planet)
    production = max(planet.jobs[PopulationJobs.FARMERS], production)
    return int(production)


#####################################################################################################
def food_cost(planet: "Planet") -> int:
    return planet.current_population()


#####################################################################################################
def empire_food(empire: "Empire") -> int:
    """How much food is being made across the empire"""
    return sum(food_surplus(planet) for planet in empire.owned_planets)
