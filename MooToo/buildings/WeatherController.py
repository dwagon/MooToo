from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingWeatherController(PlanetBuilding):

    def __init__(self):
        super().__init__("Weather Controller", Building.WEATHER_CONTROLLER)
        self.maintenance = 3
        self.cost = 200
