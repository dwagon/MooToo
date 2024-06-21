from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingGalacticCybernet(PlanetBuilding):

    def __init__(self):
        super().__init__("Galactic Cybernet", Building.GALACTIC_CYBERNET)
        self.maintenance = 3
        self.cost = 250
