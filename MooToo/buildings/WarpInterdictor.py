from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingWarpInterdictor(PlanetBuilding):

    def __init__(self):
        super().__init__("Warp Interdictor")
        self.maintenance = 3
        self.cost = 300
