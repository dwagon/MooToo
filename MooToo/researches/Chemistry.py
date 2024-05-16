from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.CHEMISTRY


#####################################################################################################
class ResearchNuclearMissile(Research):
    def __init__(self):
        super().__init__("Nuclear Missile", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class StandardFuelCells(Research):
    def __init__(self):
        super().__init__("Standard Fuel Cells", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ExtendedFuelTanks(Research):
    def __init__(self):
        super().__init__("Extended Fuel Tanks", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class TitaniumArmour(Research):
    def __init__(self):
        super().__init__("Titanium Armour", RESEARCH_POINTS, CATEGORY)
