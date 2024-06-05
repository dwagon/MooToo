from MooToo.research import Research, ResearchCategory
from MooToo.buildings.FighterGarrison import BuildingFighterGarrison
from MooToo.buildings.ArmourBarracks import BuildingArmourBarracks
from MooToo.buildings.SpacePort import BuildingSpacePort
from MooToo.constants import Technology

RESEARCH_POINTS = 400
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchSpacePort(Research):
    def __init__(self):
        super().__init__("Space Port", Technology.SPACE_PORT, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingSpacePort()


#####################################################################################################
class ResearchArmourBarracks(Research):
    def __init__(self):
        super().__init__("Armour Barracks", Technology.ARMOUR_BARRACKS, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingArmourBarracks()


#####################################################################################################
class ResearchFighterGarrison(Research):
    def __init__(self):
        super().__init__("Fighter Garrison", Technology.FIGHTER_GARRISON, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingFighterGarrison()
