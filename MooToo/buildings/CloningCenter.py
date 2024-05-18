from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingCloningCenter(PlanetBuilding):

    def __init__(self):
        super().__init__("Cloning Center")
        self.maintenance = 2
        self.cost = 100
