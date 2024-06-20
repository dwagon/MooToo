from MooToo.research import Research, TechCategory
from MooToo.buildings.SubterraneanFarms import BuildingSubterraneanFarms
from MooToo.buildings.WeatherController import BuildingWeatherController
from MooToo.constants import Technology

RESEARCH_POINTS = 1500
CATEGORY = TechCategory.BIOLOGY


#####################################################################################################
class ResearchSubterraneanFarms(Research):
    def __init__(self):
        super().__init__("Subterranean Farms ", Technology.SUBTERRANEAN_FARMS, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingSubterraneanFarms()


#####################################################################################################
class ResearchWeatherController(Research):
    def __init__(self):
        super().__init__("Weather Controller", Technology.WEATHER_CONTROLLER, RESEARCH_POINTS, CATEGORY)
        self.enabled_building = BuildingWeatherController()
