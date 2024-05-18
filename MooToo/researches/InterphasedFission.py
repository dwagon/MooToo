from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 10000
CATEGORY = ResearchCategory.POWER


#####################################################################################################
class ResearchInterphasedDrive(Research):
    def __init__(self):
        super().__init__("Interphased Drive", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPlasmaTorpedo(Research):
    def __init__(self):
        super().__init__("Plasma Torpedo", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchNeutroniumBomb(Research):
    def __init__(self):
        super().__init__("NeutroniumBomb", RESEARCH_POINTS, CATEGORY)
