from typing import TYPE_CHECKING, Any

from MooToo.planet_food import food_per, food_cost, food_surplus
from MooToo.planet_money import money_production, money_cost
from MooToo.planet_science import science_per, science_production
from MooToo.planet_work import work_per, work_cost, work_surplus
from MooToo.constants import PopulationJobs

if TYPE_CHECKING:
    from MooToo.planet import Planet


#####################################################################################################
def planet_serializer(planet: "Planet") -> dict[str, Any]:
    return {
        "id": planet.id,
        "system_id": planet.system_id,
        "name": planet.name,
        "category": planet.category,
        "owner": planet.owner,
        "size": planet.size,
        "richness": planet.richness,
        "climate": planet.climate,
        "gravity": planet.gravity,
        "arc": planet.arc,
        "climate_image": planet.climate_image,
        "morale": planet.morale(),
        "max_pop": planet.max_population(),
        "population": planet.current_population(),
        "raw_population": planet.raw_population,
        "population_increment": planet.population_increment(),
        "money_production": money_production(planet),
        "money_cost": money_cost(planet),
        "food_per": food_per(planet),
        "food_cost": food_cost(planet),
        "food_surplus": food_surplus(planet),
        "work_per": work_per(planet),
        "work_cost": work_cost(planet),
        "work_surplus": work_surplus(planet),
        "buildings": planet.buildings,
        "science_per": science_per(planet),
        "science_production": science_production(planet),
        "jobs": {
            PopulationJobs.FARMERS: planet.jobs[PopulationJobs.FARMERS],
            PopulationJobs.WORKERS: planet.jobs[PopulationJobs.WORKERS],
            PopulationJobs.SCIENTISTS: planet.jobs[PopulationJobs.SCIENTISTS],
        },
        "build_queue": [],
    }
