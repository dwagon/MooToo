from MooToo.research import Research, ResearchCategory
from MooToo.buildings.HydroponicFarm import BuildingHydroponicFarm

RESEARCH_POINTS = 1500
CATEGORY = ResearchCategory.BIOLOGY


#####################################################################################################
class ResearchSubterraneanFarms(Research):
    def __init__(self):
        super().__init__("Subterranean Farms ", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()


#####################################################################################################
class ResearchWeatherController(Research):
    def __init__(self):
        super().__init__("Weather Controller", RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingHydroponicFarm()
