from MooToo.research import Research, ResearchCategory
from MooToo.buildings.AlienManagementCenter import BuildingAlienManagementCenter

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchXenoPsychology(Research):
    def __init__(self):
        super().__init__("Xeno Psychology", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchAlienManagementCenter(Research):
    def __init__(self):
        super().__init__("Alien Management Center", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingAlienManagementCenter()
