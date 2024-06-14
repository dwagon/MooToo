_buildings: dict["Building", "PlanetBuilding"]  # = load_buildings()
_researches: dict["Technology", "Research"]  # = load_researches()

from MooToo.utils import (
    load_buildings,
    load_researches,
    get_distance,
    get_distance_tuple,
    prob_map,
    get_research,
    get_building,
)
from MooToo.constants import (
    Building,
    Technology,
    PlanetClimate,
    PlanetSize,
    PlanetCategory,
    PlanetRichness,
    PlanetGravity,
    PopulationJobs,
    StarColour,
)
from MooToo.names import empire_names, system_names
from MooToo.galaxy import Galaxy, load, save
from MooToo.system import System, StarColour
from MooToo.construct import Construct, ConstructType
from MooToo.ship import Ship, ShipType, select_ship_type_by_name
from MooToo.planet import Planet, make_home_planet
from MooToo.empire import Empire
from MooToo.planet_building import PlanetBuilding
from MooToo.research import Research, TechCategory

_buildings = load_buildings()
_researches = load_researches()
