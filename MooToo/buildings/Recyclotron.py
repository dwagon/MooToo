from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingRecyclotron(PlanetBuilding):

    def __init__(self):
        super().__init__("Recyclotron")
        self.maintenance = 3
        self.cost = 200
