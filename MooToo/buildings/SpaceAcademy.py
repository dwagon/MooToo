from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingSpaceAcademy(PlanetBuilding):

    def __init__(self):
        super().__init__("Space Academy")
        self.maintenance = 2
        self.cost = 100
