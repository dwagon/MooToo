from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingWarpInterdictor(PlanetBuilding):

    def __init__(self):
        super().__init__("Warp Interdictor", Building.WARP_INTERDICTOR)
        self.maintenance = 3
        self.cost = 300
