from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingHousing(PlanetBuilding):

    def __init__(self):
        super().__init__("Housing", Building.HOUSING)
        self.maintenance = 0
        self.cost = 99999999
