from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchStealthField(Research):
    def __init__(self):
        super().__init__("Stealth Field", Technology.STEALTH_FIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPersonalShield(Research):
    def __init__(self):
        super().__init__("Personal Shield", Technology.PERSONAL_SHIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStealthSuit(Research):
    def __init__(self):
        super().__init__("Stealth Suit", Technology.STEALTH_SUIT, RESEARCH_POINTS, CATEGORY)
