from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 150
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchFusionBeam(Research):
    def __init__(self):
        super().__init__("Fusion Beam", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchFusionRifle(Research):
    def __init__(self):
        super().__init__("Fusion Rifle", RESEARCH_POINTS, CATEGORY)
