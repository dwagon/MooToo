from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 250
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchDeuteriumFuelCells(Research):
    def __init__(self):
        super().__init__("Deuterium Fuel Cells", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchTritaniumArmour(Research):
    def __init__(self):
        super().__init__("Tritanium Armour", RESEARCH_POINTS, CATEGORY)
