from typing import TYPE_CHECKING
from MooToo.constants import PopulationJobs, Building
from MooToo.utils import get_building
from MooToo.planet_work import work_surplus

if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
def money_production(planet: "Planet") -> int:
    """How much money the planet produces"""
    money = (
        planet.jobs[PopulationJobs.FARMERS]
        + planet.jobs[PopulationJobs.WORKERS]
        + planet.jobs[PopulationJobs.SCIENTISTS]
    )
    if planet.build_queue.is_building(Building.TRADE_GOODS):
        money += work_surplus(planet)
    return money


#####################################################################################################
def money_cost(planet: "Planet") -> int:
    """How much money the planet costs"""
    return sum(get_building(_).maintenance for _ in planet.buildings)


#####################################################################################################
def money_surplus(planet: "Planet") -> int:
    return money_production(planet) - money_cost(planet)
