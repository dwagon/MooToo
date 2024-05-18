from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingCoreWasteDump(PlanetBuilding):

    def __init__(self):
        super().__init__("CoreWasteDump")
        self.maintenance = 8
        self.cost = 200
