from enum import Enum, auto

URL = "http://localhost:8000"


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    PLANET = auto()
    ORBIT = auto()
    SCIENCE = auto()
    FLEET = auto()
    COLONY_SUM = auto()
    PLANET_SUM = auto()
    PLANET_BUILD = auto()
    PLANET_DETAILS = auto()
