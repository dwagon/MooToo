from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingGaiaTransformation(PlanetBuilding):

    def __init__(self):
        super().__init__("Gaia Transformation", Building.GAIA_TRANSFORMATION)
        self.maintenance = 0
        self.cost = 500
