from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingDimensionalPortal(PlanetBuilding):

    def __init__(self):
        super().__init__("Dimensional Portal")
        self.maintenance = 2
        self.cost = 500
