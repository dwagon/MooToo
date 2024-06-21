from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingGroundBatteries(PlanetBuilding):

    def __init__(self):
        super().__init__("Ground Batteries", Building.GROUND_BATTERIES)
        self.maintenance = 2
        self.cost = 200
