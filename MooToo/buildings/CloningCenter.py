from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingCloningCenter(PlanetBuilding):

    def __init__(self):
        super().__init__("Cloning Center", Building.CLONING_CENTER)
        self.maintenance = 2
        self.cost = 100
