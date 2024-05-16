from MooToo.research import Research, ResearchCategory

RESEARCH_POINTS = 50
CATEGORY = ResearchCategory.SOCIOLOGY


#####################################################################################################
class ResearchMilitaryTactics(Research):
    def __init__(self):
        super().__init__("Military Tactics", RESEARCH_POINTS, CATEGORY)
        # self.enabled_building = BuildingSpaceAcademy()
