from enum import StrEnum, auto
from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Technology


class ResearchCategory(StrEnum):
    CONSTRUCTION = auto()
    POWER = auto()
    CHEMISTRY = auto()
    SOCIOLOGY = auto()
    COMPUTERS = auto()
    BIOLOGY = auto()
    PHYSICS = auto()
    FORCE_FIELDS = auto()


#####################################################################################################
#####################################################################################################
class Research:
    def __init__(self, name: str, tag: Technology, cost: int, category: ResearchCategory):
        self.name: str = name
        self.tag = tag
        self.cost: int = cost
        self.enabled_building: PlanetBuilding | None = None
        self.category: ResearchCategory = category
