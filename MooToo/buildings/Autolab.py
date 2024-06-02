from MooToo.planetbuilding import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingAutolab(PlanetBuilding):

    def __init__(self):
        super().__init__("Autolab", Building.AUTOLAB)
        self.maintenance = 3
        self.cost = 200
