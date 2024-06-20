from enum import StrEnum, auto
from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Technology


#####################################################################################################
class TechCategory(StrEnum):
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
    def __init__(self, name: str, tag: Technology, cost: int, category: TechCategory):
        self.name: str = name
        self.tag = tag
        self.cost: int = cost
        self.enabled_building: PlanetBuilding | None = None
        self.category: TechCategory = category
        self.general = []  # Techs that get learnt along with this one
