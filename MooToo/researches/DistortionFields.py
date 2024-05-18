from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 3500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchCloakingDevice(Research):
    def __init__(self):
        super().__init__("Cloaking Device", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStasisField(Research):
    def __init__(self):
        super().__init__("Stasis Field", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHardShields(Research):
    def __init__(self):
        super().__init__("Hard Shields", RESEARCH_POINTS, CATEGORY)
