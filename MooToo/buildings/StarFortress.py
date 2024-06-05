from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingStarFortress(PlanetBuilding):

    def __init__(self):
        super().__init__("Star Fortress", Building.STAR_FORTRESS)
        self.maintenance = 4
        self.cost = 2500
