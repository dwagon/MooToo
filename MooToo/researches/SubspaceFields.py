from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassVShields(Research):
    def __init__(self):
        super().__init__("Class V Shields", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMultiWaveECMJammer(Research):
    def __init__(self):
        super().__init__("Multi-Wave ECM Jammer", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGaussCannon(Research):
    def __init__(self):
        super().__init__("Gauss Cannon", RESEARCH_POINTS, CATEGORY)
