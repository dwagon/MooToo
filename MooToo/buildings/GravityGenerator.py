from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingGravityGenerator(PlanetBuilding):

    def __init__(self):
        super().__init__("Gravity Generator", Building.GRAVITY_GENERATOR)
        self.maintenance = 2
        self.cost = 120
