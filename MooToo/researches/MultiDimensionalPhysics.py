from MooToo.research import Research, ResearchCategory
from MooToo.buildings.DimensionalPortal import BuildingDimensionalPortal
from MooToo.constants import Technology

RESEARCH_POINTS = 4500
CATEGORY = ResearchCategory.PHYSICS


#####################################################################################################
class ResearchDisruptorCannon(Research):
    def __init__(self):
        super().__init__("Disruptor Cannon", Technology.DISRUPTOR_CANNON, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchDimensionalPortal(Research):
    def __init__(self):
        super().__init__("Dimensional Portal ", Technology.DIMENSIONAL_PORTAL, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingDimensionalPortal()
