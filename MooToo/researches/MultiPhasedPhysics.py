from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = TechCategory.PHYSICS


#####################################################################################################
class ResearchPhasors(Research):
    def __init__(self):
        super().__init__("Phasors", Technology.PHASORS, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchPhasorRifle(Research):
    def __init__(self):
        super().__init__("Phasor Rifle", Technology.PHASOR_RIFLE, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMultiPhasedShields(Research):
    def __init__(self):
        super().__init__("Multi-Phased Shields", Technology.MULTI_PHASED_SHIELDS, RESEARCH_POINTS, CATEGORY)
