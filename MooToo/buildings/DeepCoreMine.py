from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingDeepCoreMine(PlanetBuilding):

    def __init__(self):
        super().__init__("Deep Core Mine")
        self.maintenance = 3
        self.cost = 250
