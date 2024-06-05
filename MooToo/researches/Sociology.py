from MooToo.research import Research, ResearchCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchMilitaryTactics(Research):
    def __init__(self):
        super().__init__("Military Tactics", Technology.MILITARY_TACTICS, RESEARCH_POINTS, CATEGORY)
        # self.enabled_building = BuildingSpaceAcademy()
