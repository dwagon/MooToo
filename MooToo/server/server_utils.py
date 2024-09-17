from typing import TYPE_CHECKING
from fastapi import status, HTTPException
from ..galaxy import Galaxy
from MooToo.bigbang import create_galaxy

if TYPE_CHECKING:
    from MooToo.planet import Planet

URL_PREFIX_SHIPS = "/ships"
URL_PREFIX_SYSTEMS = "/systems"
URL_PREFIX_PLANETS = "/planets"
URL_PREFIX_EMPIRES = "/empires"
URL_PREFIX_GALAXY = "/galaxy"
URL_PREFIX_BUILD_QUEUE = "/build_queue"
URL_PREFIX_DESIGN = "/design"


GALAXY = None


#####################################################################################################
def get_galaxy():
    global GALAXY
    if not GALAXY:
        print("Creating galaxy")
        GALAXY = create_galaxy()
    yield GALAXY


#####################################################################################################
def get_safe_planet(planet_id: int, gal: Galaxy) -> "Planet":
    try:
        planet = gal.planets[planet_id]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return planet


# EOF
