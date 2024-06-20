from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 1500
CATEGORY = TechCategory.COMPUTERS


#####################################################################################################
class ResearchEmissionsGuidanceSystem(Research):
    def __init__(self):
        super().__init__("Emissions Guidance System", Technology.EMISSIONS_GUIDANCE_SYSTEM, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchRangemasterTargetingUnit(Research):
    def __init__(self):
        super().__init__("Rangemaster Targeting Unit", Technology.RANGEMASTER_TARGETING_UNIT, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchCyberSecurityLink(Research):
    def __init__(self):
        super().__init__("Cyber Security Link", Technology.CYBER_SECURITY_LINK, RESEARCH_POINTS, CATEGORY)
