from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.COMPUTERS


#####################################################################################################
class ResearchEmissionsGuidanceSystem(Research):
    def __init__(self):
        super().__init__("Emissions Guidance System", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchRangemasterTargetingUnit(Research):
    def __init__(self):
        super().__init__("Rangemaster Targeting Unit", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchCyberSecurityLink(Research):
    def __init__(self):
        super().__init__("Cyber Security Link", RESEARCH_POINTS, CATEGORY)
