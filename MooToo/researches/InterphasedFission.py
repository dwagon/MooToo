from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 10000
CATEGORY = TechCategory.POWER


#####################################################################################################
class ResearchInterphasedDrive(Research):
    def __init__(self):
        super().__init__("Interphased Drive", Technology.INTERPHASED_DRIVE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlasmaTorpedo(Research):
    def __init__(self):
        super().__init__("Plasma Torpedo", Technology.PLASMA_TORPEDO, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutroniumBomb(Research):
    def __init__(self):
        super().__init__("Neutronium Bomb", Technology.NEUTRONIUM_BOMB, RESEARCH_POINTS, CATEGORY)
