from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingStellarConverter(PlanetBuilding):

    def __init__(self):
        super().__init__("Stellar Converter")
        self.maintenance = 6
        self.cost = 1000
