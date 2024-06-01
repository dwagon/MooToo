from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchSubspaceCommunications(Research):
    def __init__(self):
        super().__init__("Subspace Communications", Technology.SUBSPACE_COMMUNICATIONS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchJumpGate(Research):
    def __init__(self):
        super().__init__("Jump Gate", Technology.JUMP_GATE, RESEARCH_POINTS, CATEGORY)
