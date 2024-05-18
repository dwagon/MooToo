from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingWeatherController(PlanetBuilding):

    def __init__(self):
        super().__init__("Weather Controller")
        self.maintenance = 3
        self.cost = 200
