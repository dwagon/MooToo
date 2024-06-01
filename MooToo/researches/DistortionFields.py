from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchCloakingDevice(Research):
    def __init__(self):
        super().__init__("Cloaking Device", Technology.CLOAKING_DEVICE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStasisField(Research):
    def __init__(self):
        super().__init__("Stasis Field", Technology.STASIS_FIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHardShields(Research):
    def __init__(self):
        super().__init__("Hard Shields", Technology.HARD_SHIELDS, RESEARCH_POINTS, CATEGORY)
