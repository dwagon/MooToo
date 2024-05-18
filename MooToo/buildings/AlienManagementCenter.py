from MooToo.planetbuilding import PlanetBuilding


#####################################################################################################
class BuildingAlienManagementCenter(PlanetBuilding):

    def __init__(self):
        super().__init__("Alien Management Center")
        self.maintenance = 1
        self.cost = 60
