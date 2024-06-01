from MooToo.research import Research, ResearchCategory
from MooToo.buildings.GroundBatteries import BuildingGroundBatteries
from MooToo.constants import Technology


RESEARCH_POINTS = 1150
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchTitanConstruction(Research):
    def __init__(self):
        super().__init__("Titan Construction", Technology.TITAN_CONSTRUCTION, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchGroundBatteries(Research):
    def __init__(self):
        super().__init__("Ground Batteries", Technology.GROUND_BATTERIES, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingGroundBatteries()


#####################################################################################################
class ResearchBattleoids(Research):
    def __init__(self):
        super().__init__("Battleoids", Technology.BATTLEOIDS, RESEARCH_POINTS, CATEGORY)
