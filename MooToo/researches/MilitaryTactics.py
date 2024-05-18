from MooToo.research import Research, ResearchCategory
from MooToo.buildings.SpaceAcademy import BuildingSpaceAcademy

RESEARCH_POINTS = 150
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchSpaceAcademy(Research):
    def __init__(self):
        super().__init__("Space Academy", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingSpaceAcademy()
