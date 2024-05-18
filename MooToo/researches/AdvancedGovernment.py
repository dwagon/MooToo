from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchAdvancedGovernment(Research):
    def __init__(self):
        super().__init__("AdvancedGovernment", RESEARCH_POINTS, CATEGORY)
