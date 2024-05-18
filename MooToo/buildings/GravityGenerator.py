from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingGravityGenerator(PlanetBuilding):

    def __init__(self):
        super().__init__("Gravity Generator")
        self.maintenance = 2
        self.cost = 120
