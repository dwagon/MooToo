from MooToo.research import Research, ResearchCategory
from MooToo.buildings.FighterGarrison import BuildingFighterGarrison
from MooToo.buildings.ArmourBarracks import BuildingArmourBarracks
from MooToo.buildings.SpacePort import BuildingSpacePort

RESEARCH_POINTS = 400
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchSpacePort(Research):
    def __init__(self):
        super().__init__("Space Port", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingSpacePort()


#####################################################################################################
class ResearchArmourBarracks(Research):
    def __init__(self):
        super().__init__("Armour Barracks", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingArmourBarracks()


#####################################################################################################
class ResearchFighterGarrison(Research):
    def __init__(self):
        super().__init__("Fighter Garrison", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingFighterGarrison()
