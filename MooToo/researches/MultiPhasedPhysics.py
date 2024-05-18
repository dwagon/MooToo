from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchPhasors(Research):
    def __init__(self):
        super().__init__("Phasors", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPhasorRifle(Research):
    def __init__(self):
        super().__init__("Phasor Rifle", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMultiPhasedShields(Research):
    def __init__(self):
        super().__init__("Multi-Phased Shields", RESEARCH_POINTS, CATEGORY)
