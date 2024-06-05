from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 150
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchFusionBeam(Research):
    def __init__(self):
        super().__init__("Fusion Beam", Technology.FUSION_BEAM, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFusionRifle(Research):
    def __init__(self):
        super().__init__("Fusion Rifle", Technology.FUSION_RIFLE, RESEARCH_POINTS, CATEGORY)
