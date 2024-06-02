from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingStellarConverter(PlanetBuilding):

    def __init__(self):
        super().__init__("Stellar Converter", Building.STELLAR_CONVERTER)
        self.maintenance = 6
        self.cost = 1000
