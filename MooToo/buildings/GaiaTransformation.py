from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingGaiaTransformation(PlanetBuilding):

    def __init__(self):
        super().__init__("Gaia Transformation")
        self.maintenance = 0
        self.cost = 500
