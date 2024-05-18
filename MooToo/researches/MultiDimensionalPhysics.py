from MooToo.research import Research, ResearchCategory
from MooToo.buildings.DimensionalPortal import BuildingDimensionalPortal

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchDisruptorCannon(Research):
    def __init__(self):
        super().__init__("Disruptor Cannon", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchDimensionalPortal(Research):
    def __init__(self):
        super().__init__("Dimensional Portal ", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingDimensionalPortal()
