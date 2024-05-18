from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingSubterraneanFarms(PlanetBuilding):

    def __init__(self):
        super().__init__("Subterranean Farms")
        self.maintenance = 4
        self.cost = 150
