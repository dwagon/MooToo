from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingAutolab(PlanetBuilding):

    def __init__(self):
        super().__init__("Autolab")
        self.maintenance = 3
        self.cost = 200
