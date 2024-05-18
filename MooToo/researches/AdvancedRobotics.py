from MooToo.research import Research, ResearchCategory
from MooToo.buildings.RoboticFactory import BuildingRoboticFactory

RESEARCH_POINTS = 2000
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchRoboticFactory(Research):
    def __init__(self):
        super().__init__("Robotic Factory", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingRoboticFactory()


#####################################################################################################
class ResearchBomberBays(Research):
    def __init__(self):
        super().__init__("Bomber Bays", RESEARCH_POINTS, CATEGORY)
