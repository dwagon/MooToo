from MooToo.research import Research, TechCategory
from MooToo.buildings.StarFortress import BuildingStarFortress
from MooToo.constants import Technology

RESEARCH_POINTS = 6000
CATEGORY = TechCategory.CONSTRUCTION


#####################################################################################################
class ResearchStarFortress(Research):
    def __init__(self):
        super().__init__("Star Fortress", Technology.STAR_FORTRESS, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingStarFortress()


#####################################################################################################
class ResearchAdvancedCityPlanning(Research):
    def __init__(self):
        super().__init__("Advanced City Planning", Technology.ADVANCED_CITY_PLANNING, RESEARCH_POINTS, CATEGORY)


#####################################################################################################
class ResearchHeavyFighters(Research):
    def __init__(self):
        super().__init__("Heavy Fighters", Technology.HEAVY_FIGHTERS, RESEARCH_POINTS, CATEGORY)
