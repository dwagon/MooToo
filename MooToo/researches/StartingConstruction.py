from MooToo.research import Research, ResearchCategory
from MooToo.buildings.MarineBarracks import BuildingMarineBarracks

RESEARCH_POINTS = 0
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchColonyBase(Research):
    def __init__(self):
        super().__init__("Colony Base", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchStarBase(Research):
    def __init__(self):
        super().__init__("Star Base", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchMarineBarracks(Research):
    def __init__(self):
        super().__init__("Marine Barracks", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingMarineBarracks()
