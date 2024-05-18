from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchStealthField(Research):
    def __init__(self):
        super().__init__("Stealth Field", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPersonalShield(Research):
    def __init__(self):
        super().__init__("Personal Shield", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStealthSuit(Research):
    def __init__(self):
        super().__init__("Stealth Suit", RESEARCH_POINTS, CATEGORY)
