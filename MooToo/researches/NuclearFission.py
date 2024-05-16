from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchFreighters(Research):
    def __init__(self):
        super().__init__("Freighters", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNuclearDrive(Research):
    def __init__(self):
        super().__init__("Nuclear Drive", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNuclearBomb(Research):
    def __init__(self):
        super().__init__("Nuclear Bomb", RESEARCH_POINTS, CATEGORY)
