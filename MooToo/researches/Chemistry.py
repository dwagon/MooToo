from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.CHEMISTRY
general = [
    Technology.NUCLEAR_MISSILE,
    Technology.STANDARD_FUEL_CELLS,
    Technology.EXTENDED_FUEL_TANKS,
    Technology.TITANIUM_ARMOUR,
]


#####################################################################################################
class ResearchNuclearMissile(Research):
    def __init__(self):
        super().__init__("Nuclear Missile", Technology.NUCLEAR_MISSILE, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class StandardFuelCells(Research):
    def __init__(self):
        super().__init__("Standard Fuel Cells", Technology.STANDARD_FUEL_CELLS, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ExtendedFuelTanks(Research):
    def __init__(self):
        super().__init__("Extended Fuel Tanks", Technology.EXTENDED_FUEL_TANKS, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class TitaniumArmour(Research):
    def __init__(self):
        super().__init__("Titanium Armour", Technology.TITANIUM_ARMOUR, RESEARCH_POINTS, CATEGORY)
        self.general = general
