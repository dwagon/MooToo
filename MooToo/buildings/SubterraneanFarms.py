from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingSubterraneanFarms(PlanetBuilding):

    def __init__(self):
        super().__init__("Subterranean Farms", Building.SUBTERRANEAN_FARM)
        self.maintenance = 4
        self.cost = 150
