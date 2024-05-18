from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchSubspaceCommunications(Research):
    def __init__(self):
        super().__init__("Subspace Communications", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchJumpGate(Research):
    def __init__(self):
        super().__init__("Jump Gate", RESEARCH_POINTS, CATEGORY)
