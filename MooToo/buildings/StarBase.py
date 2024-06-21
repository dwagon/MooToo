from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingStarBase(PlanetBuilding):

    def __init__(self):
        super().__init__("Star Base", Building.STAR_BASE)
        self.maintenance = 2
        self.cost = 400
