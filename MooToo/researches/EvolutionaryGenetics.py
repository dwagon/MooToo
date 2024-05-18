from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchPsionics(Research):
    def __init__(self):
        super().__init__("Psionics", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHeightenedIntelligence(Research):
    def __init__(self):
        super().__init__("Heightened Intelligence", RESEARCH_POINTS, CATEGORY)
