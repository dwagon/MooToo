from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingAlienManagementCenter(PlanetBuilding):

    def __init__(self):
        super().__init__("Alien Management Center", Building.ALIEN_MANAGEMENT_CENTER)
        self.maintenance = 1
        self.cost = 60
