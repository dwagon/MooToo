from MooToo.research import Research, TechCategory
from MooToo.buildings.SpaceAcademy import BuildingSpaceAcademy
from MooToo.constants import Technology

RESEARCH_POINTS = 150
CATEGORY = TechCategory.SOCIOLOGY


#####################################################################################################
class ResearchSpaceAcademy(Research):
    def __init__(self):
        super().__init__("Space Academy", Technology.SPACE_ACADEMY, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingSpaceAcademy()
