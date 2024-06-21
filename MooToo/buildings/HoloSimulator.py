from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingHoloSimulator(PlanetBuilding):

    def __init__(self):
        super().__init__("Holo Simulator", Building.HOLO_SIMULATOR)
        self.maintenance = 1
        self.cost = 120
