from MooToo.research import Research, ResearchCategory
from MooToo.buildings.ArtemisSystemNet import BuildingArtemisSystemNet

RESEARCH_POINTS = 7500
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchDoomStarConstruction(Research):
    def __init__(self):
        super().__init__("Doom Star Construction", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchArtemisSystemNet(Research):
    def __init__(self):
        super().__init__("Artemis System Net", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingArtemisSystemNet()
