from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 10000
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchThoriumFuelCells(Research):
    def __init__(self):
        super().__init__("Thorium Fuel Cells", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAdamantiumArmor(Research):
    def __init__(self):
        super().__init__("Adamantium Armor", RESEARCH_POINTS, CATEGORY)
