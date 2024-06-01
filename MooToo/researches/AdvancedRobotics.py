from MooToo.research import Research, ResearchCategory
from MooToo.buildings.RoboticFactory import BuildingRoboticFactory
from MooToo.constants import Technology

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchRoboticFactory(Research):
    def __init__(self):
        super().__init__("Robotic Factory", Technology.ROBOTIC_FACTORY, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingRoboticFactory()


#####################################################################################################
class ResearchBomberBays(Research):
    def __init__(self):
        super().__init__("Bomber Bays", Technology.BOMBER_BAYS, RESEARCH_POINTS, CATEGORY)
