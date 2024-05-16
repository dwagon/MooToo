from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingStarBase(PlanetBuilding):

    def __init__(self):
        super().__init__("Star Base")
        self.maintenance = 2
        self.cost = 400
