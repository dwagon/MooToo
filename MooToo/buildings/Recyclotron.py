from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingRecyclotron(PlanetBuilding):

    def __init__(self):
        super().__init__("Recyclotron", Building.RECYCLOTRON)
        self.maintenance = 3
        self.cost = 200
