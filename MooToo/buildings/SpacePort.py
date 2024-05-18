from MooToo.planetbuilding import PlanetBuilding
from MooToo.planet import Planet


#####################################################################################################
class BuildingSpacePort(PlanetBuilding):

    def __init__(self):
        super().__init__("Space Port")
        self.maintenance = 1
        self.cost = 80
