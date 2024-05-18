from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchZeonMissile(Research):
    def __init__(self):
        super().__init__("Zeon Missile", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutroniumArmour(Research):
    def __init__(self):
        super().__init__("Neutronium Armour", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchUridiumFuelCells(Research):
    def __init__(self):
        super().__init__("Uridium Fuel Cells", RESEARCH_POINTS, CATEGORY)
