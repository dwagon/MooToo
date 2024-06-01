from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchAdvancedGovernment(Research):
    def __init__(self):
        super().__init__("AdvancedGovernment", Technology.ADVANCED_GOVERNMENT, RESEARCH_POINTS, CATEGORY)
