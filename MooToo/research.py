from enum import StrEnum, auto
from MooToo.planetbuilding import PlanetBuilding


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
    def __init__(self, name: str, cost: int, category: ResearchCategory):
        self.name: str = name
        self.cost: int = cost
        self.enabled_building: PlanetBuilding | None = None
        self.category: ResearchCategory = category
