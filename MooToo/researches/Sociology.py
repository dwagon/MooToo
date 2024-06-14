from MooToo.research import Research, TechCategory
from MooToo.constants import Technology

RESEARCH_POINTS = 50
CATEGORY = TechCategory.SOCIOLOGY


#####################################################################################################
class ResearchMilitaryTactics(Research):
    def __init__(self):
        super().__init__("Military Tactics", Technology.MILITARY_TACTICS, RESEARCH_POINTS, CATEGORY)
        # self.enabled_building = BuildingSpaceAcademy()
