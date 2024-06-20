from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingSupercomputer(PlanetBuilding):

    def __init__(self):
        super().__init__("Supercomputer", Building.SUPERCOMPUTER)
        self.maintenance = 2
        self.cost = 150
