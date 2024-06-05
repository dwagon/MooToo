from MooToo.research import Research, ResearchCategory
from MooToo.buildings.StellarConverter import BuildingStellarConverter
from MooToo.constants import Technology

RESEARCH_POINTS = 15000
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchTimeWarpFacilitator(Research):
    def __init__(self):
        super().__init__("Time Warp Facilitator", Technology.TIME_WARP_FACILITATOR, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStellarConverter(Research):
    def __init__(self):
        super().__init__("Stellar Converter", Technology.STELLAR_CONVERTER, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStellarConverter()


#####################################################################################################
class ResearchStarGate(Research):
    def __init__(self):
        super().__init__("Star Gate", Technology.STAR_GATE, RESEARCH_POINTS, CATEGORY)
