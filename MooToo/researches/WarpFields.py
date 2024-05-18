from MooToo.research import Research, ResearchCategory
from MooToo.buildings.WarpInterdictor import BuildingWarpInterdictor

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.FORCE_FIELDS


#####################################################################################################
class ResearchPulsar(Research):
    def __init__(self):
        super().__init__("Pulsar", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchWarpInterdictor(Research):
    def __init__(self):
        super().__init__("Warp Interdictor", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingWarpInterdictor()


#####################################################################################################
class ResearchLightningField(Research):
    def __init__(self):
        super().__init__("Lightning Field", RESEARCH_POINTS, CATEGORY)
