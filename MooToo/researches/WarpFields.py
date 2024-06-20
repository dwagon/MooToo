from MooToo.research import Research, TechCategory
from MooToo.buildings.WarpInterdictor import BuildingWarpInterdictor
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = TechCategory.FORCE_FIELDS


#####################################################################################################
class ResearchPulsar(Research):
    def __init__(self):
        super().__init__("Pulsar", Technology.PULSAR, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchWarpInterdictor(Research):
    def __init__(self):
        super().__init__("Warp Interdictor", Technology.WARP_INTERDICTOR, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingWarpInterdictor()


#####################################################################################################
class ResearchLightningField(Research):
    def __init__(self):
        super().__init__("Lightning Field", Technology.LIGHTNING_FIELD, RESEARCH_POINTS, CATEGORY)
