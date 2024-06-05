from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchZeonMissile(Research):
    def __init__(self):
        super().__init__("Zeon Missile", Technology.ZEON_MISSILE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutroniumArmour(Research):
    def __init__(self):
        super().__init__("Neutronium Armour", Technology.NEUTRONIUM_ARMOUR, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchUridiumFuelCells(Research):
    def __init__(self):
        super().__init__("Uridium Fuel Cells", Technology.URIDIUM_FUEL_CELLS, RESEARCH_POINTS, CATEGORY)
