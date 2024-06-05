from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchAntiMatterDrive(Research):
    def __init__(self):
        super().__init__("Anti-Matter Drive", Technology.ANTI_MATTER_DRIVE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAntiMatterTorpedoes(Research):
    def __init__(self):
        super().__init__("Anti-Matter Torpedoes", Technology.ANTI_MATTER_TORPEDOES, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAntiMatterBomb(Research):
    def __init__(self):
        super().__init__("Anti-Matter Bomb", Technology.ANTI_MATTER_BOMB, RESEARCH_POINTS, CATEGORY)
