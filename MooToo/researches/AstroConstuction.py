from MooToo.research import Research, ResearchCategory
from MooToo.buildings.GroundBatteries import BuildingGroundBatteries


RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchTitanConstruction(Research):
    def __init__(self):
        super().__init__("Titan Construction", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGroundBatteries(Research):
    def __init__(self):
        super().__init__("Ground Batteries", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingGroundBatteries()


#####################################################################################################
class ResearchBattleoids(Research):
    def __init__(self):
        super().__init__("Assault Shuttles", RESEARCH_POINTS, CATEGORY)
