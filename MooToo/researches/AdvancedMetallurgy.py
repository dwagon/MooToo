from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 250
CATEGORY = TechCategory.CHEMISTRY


#####################################################################################################
class ResearchDeuteriumFuelCells(Research):
    def __init__(self):
        super().__init__("Deuterium Fuel Cells", Technology.DEUTERIUM_FUEL_CELLS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTritaniumArmour(Research):
    def __init__(self):
        super().__init__("Tritanium Armour", Technology.TRITANIUM_ARMOUR, RESEARCH_POINTS, CATEGORY)
