from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchPsionics(Research):
    def __init__(self):
        super().__init__("Psionics", Technology.PSIONICS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHeightenedIntelligence(Research):
    def __init__(self):
        super().__init__("Heightened Intelligence", Technology.HEIGHTENED_INTELLIGENCE, RESEARCH_POINTS, CATEGORY)
