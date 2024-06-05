from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 2750
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchClassVShields(Research):
    def __init__(self):
        super().__init__("Class V Shields", Technology.CLASS_V_SHIELD, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMultiWaveECMJammer(Research):
    def __init__(self):
        super().__init__("Multi-Wave ECM Jammer", Technology.MULTI_WAVE_ECM_JAMMER, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGaussCannon(Research):
    def __init__(self):
        super().__init__("Gauss Cannon", Technology.GAUSS_CANNON, RESEARCH_POINTS, CATEGORY)
