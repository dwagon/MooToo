from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = TechCategory.SOCIOLOGY


#####################################################################################################
class ResearchAdvancedGovernment(Research):
    def __init__(self):
        super().__init__("AdvancedGovernment", Technology.ADVANCED_GOVERNMENT, RESEARCH_POINTS, CATEGORY)
