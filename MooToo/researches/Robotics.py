from MooToo.research import Research, ResearchCategory
from MooToo.buildings.RoboMiners import BuildingRoboMiners
from MooToo.buildings.Battlestation import BuildingBattlestation

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchRoboMiners(Research):
    def __init__(self):
        super().__init__("Robo-Miners", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingRoboMiners()


#####################################################################################################
class ResearchBattlestation(Research):
    def __init__(self):
        super().__init__("Battlestation", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingBattlestation()


#####################################################################################################
class ResearchPoweredArmour(Research):
    def __init__(self):
        super().__init__("Powered Armour", RESEARCH_POINTS, CATEGORY)
