from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 10000
CATEGORY = TechCategory.CHEMISTRY


#####################################################################################################
class ResearchThoriumFuelCells(Research):
    def __init__(self):
        super().__init__("Thorium Fuel Cells", Technology.THORIUM_FUEL_CELLS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAdamantiumArmor(Research):
    def __init__(self):
        super().__init__("Adamantium Armor", Technology.ADAMANTIUM_ARMOUR, RESEARCH_POINTS, CATEGORY)
