from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.POWER
general = [Technology.FREIGHTERS, Technology.NUCLEAR_DRIVE, Technology.NUCLEAR_BOMB]


#####################################################################################################
class ResearchFreighters(Research):
    def __init__(self):
        super().__init__("Freighters", Technology.FREIGHTERS, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ResearchNuclearDrive(Research):
    def __init__(self):
        super().__init__("Nuclear Drive", Technology.NUCLEAR_DRIVE, RESEARCH_POINTS, CATEGORY)
        self.general = general


#####################################################################################################
class ResearchNuclearBomb(Research):
    def __init__(self):
        super().__init__("Nuclear Bomb", Technology.NUCLEAR_BOMB, RESEARCH_POINTS, CATEGORY)
        self.general = general
