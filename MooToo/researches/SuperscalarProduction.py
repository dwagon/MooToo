from MooToo.research import Research, ResearchCategory
from MooToo.buildings.StarFortress import BuildingStarFortress

RESEARCH_POINTS = 6000
CATEGORY = ResearchCategory.CONSTRUCTION


#####################################################################################################
class ResearchStarFortress(Research):
    def __init__(self):
        super().__init__("Star Fortress", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStarFortress()


#####################################################################################################
class ResearchAdvancedCityPlanning(Research):
    def __init__(self):
        super().__init__("AdvancedCityPlanning", RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHeavyFighters(Research):
    def __init__(self):
        super().__init__("Heavy Fighters", RESEARCH_POINTS, CATEGORY)
