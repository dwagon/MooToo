from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingSpacePort(PlanetBuilding):

    def __init__(self):
        super().__init__("Space Port", Building.SPACE_PORT)
        self.maintenance = 1
        self.cost = 80
