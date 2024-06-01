from MooToo.research import Research, ResearchCategory
from MooToo.buildings.AlienManagementCenter import BuildingAlienManagementCenter
from MooToo.constants import Technology

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchXenoPsychology(Research):
    def __init__(self):
        super().__init__("Xeno Psychology", Technology.XENO_PSYCHOLOGY, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAlienManagementCenter(Research):
    def __init__(self):
        super().__init__("Alien Management Center", Technology.ALIEN_MANAGEMENT_CENTER, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAlienManagementCenter()
