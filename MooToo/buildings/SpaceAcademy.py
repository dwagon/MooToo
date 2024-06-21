from MooToo.planet_building import PlanetBuilding
from MooToo.constants import Building


#####################################################################################################
class BuildingSpaceAcademy(PlanetBuilding):

    def __init__(self):
        super().__init__("Space Academy", Building.SPACE_ACADEMY)
        self.maintenance = 2
        self.cost = 100
