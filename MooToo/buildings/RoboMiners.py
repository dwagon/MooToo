from MooToo.ui.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingRoboMiners(PlanetBuilding):

    def __init__(self):
        super().__init__("Robo-Miners", Building.ROBO_MINERS)
        self.maintenance = 2
        self.cost = 150
