from MooToo.research import Research, ResearchCategory
from MooToo.buildings.StellarConverter import BuildingStellarConverter

RESEARCH_POINTS = 15000
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchTimeWarpFacilitator(Research):
    def __init__(self):
        super().__init__("Time Warp Facilitator", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStellarConverter(Research):
    def __init__(self):
        super().__init__("Stellar Converter", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStellarConverter()


#####################################################################################################
class ResearchStarGate(Research):
    def __init__(self):
        super().__init__("Star Gate", RESEARCH_POINTS, CATEGORY)
