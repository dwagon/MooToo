from MooToo.research import Research, ResearchCategory
from MooToo.buildings.RoboMiners import BuildingRoboMiners
from MooToo.buildings.Battlestation import BuildingBattlestation
from MooToo.constants import Technology

RESEARCH_POINTS = 650
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchRoboMiners(Research):
    def __init__(self):
        super().__init__("Robo-Miners", Technology.ROBO_MINERS, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingRoboMiners()


#####################################################################################################
class ResearchBattlestation(Research):
    def __init__(self):
        super().__init__("Battlestation", Technology.BATTLESTATION, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingBattlestation()


#####################################################################################################
class ResearchPoweredArmour(Research):
    def __init__(self):
        super().__init__("Powered Armour", Technology.POWERED_ARMOUR, RESEARCH_POINTS, CATEGORY)
